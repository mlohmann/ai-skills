"""Store normalized JEV results in a private local cache. No network access."""

import json
import os
from pathlib import Path
import stat
import sys
import tempfile
from datetime import datetime, timezone

from jobscout import cache_key, num, request


def validate_entry(entry, payload):
    expected = {k for k, q in payload['questions'].items() if q['type'] == 'score'}
    ev = entry['evaluation']
    if (entry['request'] != payload or entry['model'] != payload['model'] or ev.get('provider') != 'jev'
            or not isinstance(entry['raw_response'], dict) or not entry['raw_response']
            or not isinstance(ev.get('scores'), dict) or set(ev['scores']) != expected
            or not all(num(v, 0, 100) for v in ev['scores'].values())
            or not num(ev.get('confidence'), 0, 1)):
        raise ValueError('Invalid normalized JEV result')
    timestamp = datetime.fromisoformat(entry['evaluated_at'])
    if timestamp.tzinfo is None or timestamp > datetime.now(timezone.utc):
        raise ValueError('Invalid evaluation timestamp')


def use_cache(profile, job, directory, entry=None):
    # Build the request first so disabled profiles cannot read or write the cache.
    payload = request(profile, job)
    key = cache_key(payload)
    directory = Path(directory)
    if not directory.exists():
        directory.mkdir(mode=0o700)
    info = directory.lstat()
    if (not stat.S_ISDIR(info.st_mode) or info.st_uid != os.getuid()
            or stat.S_IMODE(info.st_mode) & 0o077):
        raise ValueError('Cache directory must be private and owned by the current user')
    path = directory / (key + '.json')
    if entry is not None:
        validate_entry(entry, payload)
        record = dict(entry, request_key=key)
        fd, temporary = tempfile.mkstemp(dir=directory)
        try:
            with os.fdopen(fd, 'w') as stream:
                json.dump(record, stream, allow_nan=False)
            os.replace(temporary, path)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)
        return {'status': 'stored', 'key': key}
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        with os.fdopen(fd) as stream:
            info = os.fstat(stream.fileno())
            if (not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid()
                    or stat.S_IMODE(info.st_mode) & 0o077):
                raise ValueError('Invalid cache file permissions')
            record = json.load(stream)
        validate_entry(record, payload)
        if record['request_key'] != key:
            raise ValueError('Cache key mismatch')
        return {'status': 'hit', 'key': key, 'entry': record}
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        return {'status': 'miss', 'key': key}


if __name__ == '__main__':
    try:
        if len(sys.argv) not in (4, 5):
            raise ValueError('Usage: evaluation_cache.py PROFILE JOB PRIVATE_DIRECTORY [ENTRY]')
        profile, job = [json.loads(Path(p).read_text()) for p in sys.argv[1:3]]
        entry = json.loads(Path(sys.argv[4]).read_text()) if len(sys.argv) == 5 else None
        print(json.dumps(use_cache(profile, job, sys.argv[3], entry), allow_nan=False))
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(2)
