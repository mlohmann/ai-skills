"""Check conflicting evidence and ambiguous duplicate identities."""

import copy
from datetime import date
from itertools import permutations
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/job-search-jev/scripts"))
from jobscout import rank


class DuplicateTests(unittest.TestCase):
    def setUp(self):
        self.profile = json.loads(
            (ROOT / "skills/job-search-jev/assets/profile.template.json").read_text(
                encoding="utf-8"
            )
        )
        self.job = {
            "company": "Example",
            "requisition_id": "A",
            "employer_url": "https://example.org/jobs/nurse",
            "title": "Nurse",
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

    def assert_conflict_review(self, first, second):
        for jobs in ((first, second), (second, first)):
            out = rank(self.profile, list(jobs), [], today=date(2026, 11, 15))
            self.assertEqual(out["excluded"], [])
            self.assertEqual(out["shortlist"], [])
            self.assertEqual(len(out["review"]), 1)
            self.assertEqual(out["duplicate_count"], 1)
            record = out["review"][0]
            self.assertIn(
                "duplicate_evidence_requires_consolidation", record["reasons"]
            )
            self.assertEqual([record["job"], *record["duplicate_jobs"]], list(jobs))

    def test_active_conflict_is_reviewed_in_both_orders(self):
        closed = copy.deepcopy(self.job)
        closed["active"] = False
        self.assert_conflict_review(closed, self.job)

    def test_confirmed_company_exclusion_survives_conflicting_activity(self):
        self.profile["excluded_companies"] = ["Example"]
        closed = copy.deepcopy(self.job)
        closed["active"] = False
        for jobs in ((closed, self.job), (self.job, closed)):
            out = rank(self.profile, list(jobs), [])
            self.assertEqual(len(out["excluded"]), 1)
            self.assertIn("excluded_company", out["excluded"][0]["reasons"])
            self.assertEqual(out["review"], [])

    def test_history_exclusion_survives_conflicting_activity(self):
        closed = copy.deepcopy(self.job)
        closed["active"] = False
        history = [dict(self.job, status="applied")]
        for jobs in ((closed, self.job), (self.job, closed)):
            out = rank(self.profile, list(jobs), history)
            self.assertEqual(len(out["excluded"]), 1)
            self.assertIn("application_history", out["excluded"][0]["reasons"])
            self.assertEqual(out["review"], [])

    def test_shared_evidence_failure_remains_excluded(self):
        first = copy.deepcopy(self.job)
        first["active"] = False
        second = dict(first, title="Nurse practitioner")
        for jobs in ((first, second), (second, first)):
            out = rank(self.profile, list(jobs), [])
            self.assertEqual(len(out["excluded"]), 1)
            self.assertIn("active_false", out["excluded"][0]["reasons"])
            self.assertEqual(out["review"], [])

    def test_pay_conflicts_are_reviewed(self):
        self.profile["salary"].update(minimum=100000, currency="USD")
        low = copy.deepcopy(self.job)
        low["salary"] = {
            "min": 90000,
            "max": 120000,
            "currency": "USD",
            "period": "year",
            "employer_reported": True,
        }
        high = copy.deepcopy(low)
        high["salary"]["min"] = 110000
        self.assert_conflict_review(low, high)
        self.profile["salary"]["missing"] = "exclude"
        missing = copy.deepcopy(self.job)
        self.assert_conflict_review(missing, high)

    def test_eligibility_conflicts_are_reviewed(self):
        for gate in (
            "role_eligible",
            "seniority_eligible",
            "location_eligible",
            "work_model_eligible",
        ):
            with self.subTest(gate=gate):
                rejected = copy.deepcopy(self.job)
                rejected[gate] = False
                self.assert_conflict_review(rejected, self.job)

    def test_posting_date_conflicts_are_reviewed(self):
        self.profile["max_age_days"] = 7
        stale = dict(self.job, posted_at="2026-11-01")
        fresh = dict(self.job, posted_at="2026-11-15")
        self.assert_conflict_review(stale, fresh)

    def test_ambiguous_url_alias_never_absorbs_distinct_ids(self):
        alias = copy.deepcopy(self.job)
        alias.pop("requisition_id")
        second = dict(self.job, requisition_id="B")
        for jobs in permutations((alias, self.job, second)):
            out = rank(self.profile, list(jobs), [])
            records = [
                r
                for bucket in ("qualified", "review", "excluded", "below_threshold")
                for r in out[bucket]
            ]
            self.assertEqual(
                {
                    r["job"]["requisition_id"]
                    for r in records
                    if r["job"].get("requisition_id")
                },
                {"A", "B"},
            )
            self.assertEqual(len(records), 3)
            self.assertEqual(out["duplicate_count"], 0)
            ambiguous = [r for r in out["review"] if not r["job"].get("requisition_id")]
            self.assertEqual(len(ambiguous), 1)
            self.assertIn("ambiguous_identity", ambiguous[0]["reasons"])

    def test_repeated_ambiguous_aliases_share_one_review_record(self):
        alias = copy.deepcopy(self.job)
        alias.pop("requisition_id")
        second = dict(self.job, requisition_id="B")
        updated = dict(alias, captured_at="2026-11-15")
        for jobs in (
            (alias, self.job, second, alias, updated),
            (updated, second, alias, self.job, alias),
        ):
            out = rank(self.profile, list(jobs), [])
            records = [
                r
                for bucket in ("qualified", "review", "excluded", "below_threshold")
                for r in out[bucket]
            ]
            self.assertEqual(len(records), 3)
            self.assertEqual(out["duplicate_count"], 2)
            ambiguous = [r for r in out["review"] if not r["job"].get("requisition_id")]
            self.assertEqual(len(ambiguous), 1)
            self.assertIn("ambiguous_identity", ambiguous[0]["reasons"])

    def test_distinct_ids_survive_when_company_is_missing(self):
        first = dict(self.job, company=None)
        second = dict(first, requisition_id="B")
        for jobs in permutations((first, second)):
            out = rank(self.profile, list(jobs), [])
            records = [
                r
                for bucket in ("qualified", "review", "excluded", "below_threshold")
                for r in out[bucket]
            ]
            self.assertEqual(len(records), 2)
            self.assertEqual({r["job"]["requisition_id"] for r in records}, {"A", "B"})

    def test_unambiguous_url_alias_keeps_the_explicit_id(self):
        alias = copy.deepcopy(self.job)
        alias.pop("requisition_id")
        for jobs in ((alias, self.job), (self.job, alias)):
            original = copy.deepcopy(jobs)
            out = rank(self.profile, list(jobs), [])
            self.assertEqual(out["duplicate_count"], 1)
            self.assertEqual(len(out["review"]), 1)
            self.assertEqual(out["review"][0]["job"]["requisition_id"], "A")
            self.assertEqual(out["review"][0]["duplicate_jobs"], [alias])
            self.assertEqual(jobs, original)


if __name__ == "__main__":
    unittest.main()
