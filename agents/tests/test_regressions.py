"""Regression coverage for ranking and external-JSON edge cases."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/job-search-jev/scripts"))
from jobscout import rank, validate
from evidence import collect


class ReviewRegressions(unittest.TestCase):
    def setUp(self):
        self.profile = json.loads(
            (ROOT / "skills/job-search-jev/assets/profile.template.json").read_text(
                encoding="utf-8"
            )
        )
        self.job = {
            "company": "Example",
            "requisition_id": "NEW-2",
            "employer_url": "https://example.org/careers/nurse",
            "role_eligible": True,
            "seniority_eligible": True,
            "location_eligible": True,
            "work_model_eligible": True,
            "active": True,
            "employer_verified": True,
            "evaluation": {
                "provider": "assistant",
                "scores": {c["id"]: 90 for c in self.profile["criteria"]},
            },
        }

    def test_distinct_requisition_ids_do_not_match_url_only_company_metadata(self):
        history = [
            {
                "company": None,
                "requisition_id": "OLD-1",
                "employer_url": self.job["employer_url"],
                "status": "applied",
            }
        ]
        self.assertEqual(len(rank(self.profile, [self.job], history)["shortlist"]), 1)

    def test_mixed_unit_range_requires_review_instead_of_false_amount(self):
        evidence = collect({"text": "Annual base pay USD 90–120k."})
        self.assertEqual(
            evidence["salary_candidates"],
            [],
            "Mixed-unit notation must be normalized explicitly or left unknown, never emitted as 90–120000",
        )

    def test_valid_profile_without_salary_floor_can_rank(self):
        self.profile["salary"].pop("minimum")
        validate(self.profile)
        self.assertEqual(len(rank(self.profile, [self.job], [])["shortlist"]), 1)

    def test_utf8_profile_is_read_independently_of_system_locale(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.profile["target_roles"] = ["Infirmier à Montréal"]
            profile = Path(tmp) / "profile.json"
            profile.write_text(
                json.dumps(self.profile, ensure_ascii=False), encoding="utf-8"
            )
            env = dict(os.environ, LC_ALL="C", PYTHONUTF8="0", PYTHONCOERCECLOCALE="0")
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "skills/job-search-jev/scripts/jobscout.py"),
                    "validate",
                    str(profile),
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                env=env,
            )
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_null_tool_response_has_controlled_input_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            evidence = Path(tmp) / "evidence.json"
            response = Path(tmp) / "response.json"
            evidence.write_text(
                json.dumps(collect({"text": "Base CAD 45–50 per hour"})),
                encoding="utf-8",
            )
            response.write_text("null")
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "skills/job-search-jev/scripts/evidence.py"),
                    "resolve",
                    str(evidence),
                    str(response),
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
