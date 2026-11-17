import copy
import json
from unittest.mock import patch
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/job-search-jev/scripts'))
from evaluation_cache import use_cache
from jobscout import request
from evidence import collect, extraction_request


class CacheTests(unittest.TestCase):
    def setUp(self):
        self.profile = json.loads((ROOT / 'skills/job-search-jev/assets/profile.template.json').read_text())
        self.profile['jev'].update(enabled=True, model='jev-1.2.3')
        self.job = {'title': 'Engineer', 'description': 'Build accessible interfaces'}
        self.entry = {
            'request': request(self.profile, self.job),
            'model': 'jev-1.2.3', 'evaluated_at': '2026-01-01T00:00:00+00:00',
            'raw_response': {'answers': 'fixture only'},
            'evaluation': {'provider': 'jev', 'confidence': 0.9,
                           'scores': {c['id']: 80 for c in self.profile['criteria']}}
        }

    def test_opt_in_blocks_cache_and_both_request_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            for value in (False, None):
                p = copy.deepcopy(self.profile)
                if value is None:
                    p['jev'].pop('enabled')
                else:
                    p['jev']['enabled'] = value
                for action in (lambda: use_cache(p, self.job, directory),
                               lambda: use_cache(p, self.job, directory, self.entry),
                               lambda: request(p, self.job),
                               lambda: extraction_request(collect({'text': 'Example'}), p)):
                    with self.assertRaises(ValueError):
                        action()

    def test_cache_hit_invalidation_and_permissions(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(use_cache(self.profile, self.job, directory)['status'], 'miss')
            use_cache(self.profile, self.job, directory, self.entry)
            self.assertEqual(use_cache(self.profile, self.job, directory)['status'], 'hit')
            path = next(Path(directory).glob('*.json'))
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            for field, value in [('description', 'Changed evidence'), ('title', 'Other role')]:
                changed = dict(self.job, **{field: value})
                self.assertEqual(use_cache(self.profile, changed, directory)['status'], 'miss')
            for field, value in [('candidate_evidence', ['New evidence']), ('preferences', ['New preference'])]:
                p = dict(self.profile, **{field: value})
                self.assertEqual(use_cache(p, self.job, directory)['status'], 'miss')
            for change in ('model', 'rubric'):
                p = copy.deepcopy(self.profile)
                if change == 'model':
                    p['jev']['model'] = 'jev-4.5.6'
                else:
                    p['criteria'][0]['description'] = 'Changed rubric'
                self.assertEqual(use_cache(p, self.job, directory)['status'], 'miss')
            path.write_text('{broken')
            self.assertEqual(use_cache(self.profile, self.job, directory)['status'], 'miss')
            path.unlink()
            path.symlink_to('/dev/null')
            self.assertEqual(use_cache(self.profile, self.job, directory)['status'], 'miss')

    def test_reject_invalid_entries_and_alias(self):
        with tempfile.TemporaryDirectory() as directory:
            for field, value in [('request', {}), ('model', 'jev-9.9'), ('evaluated_at', 'invalid'), ('raw_response', {})]:
                entry = dict(self.entry, **{field: value})
                with self.assertRaises(ValueError):
                    use_cache(self.profile, self.job, directory, entry)
            p = copy.deepcopy(self.profile)
            p['jev']['model'] = 'jev-latest'
            with self.assertRaises(ValueError):
                use_cache(p, self.job, directory)
            Path(directory).chmod(0o755)
            with self.assertRaises(ValueError):
                use_cache(self.profile, self.job, directory)

    def test_invalid_normalization_cannot_be_stored(self):
        with tempfile.TemporaryDirectory() as directory:
            for change in ({'confidence': None}, {'confidence': True},
                           {'scores': {}}, {'provider': 'assistant'},
                           {'scores': {c['id']: 101 for c in self.profile['criteria']}}):
                entry = copy.deepcopy(self.entry)
                entry['evaluation'].update(change)
                with self.assertRaises(ValueError):
                    use_cache(self.profile, self.job, directory, entry)
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_unsupported_host_fails_before_cache_access(self):
        with patch('evaluation_cache.os.name', 'nt'), patch('evaluation_cache.Path') as path:
            for entry in (None, self.entry):
                with self.assertRaisesRegex(ValueError, 'requires a POSIX host'):
                    use_cache(self.profile, self.job, 'unused', entry)
            path.assert_not_called()
