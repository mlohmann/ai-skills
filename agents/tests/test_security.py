import copy
import json
from pathlib import Path
import secrets
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "scripts"), str(ROOT / "skills/job-search-jev/scripts")]
import install
import package
from jobscout import request, rank, validate
from evidence import collect, extraction_request


class SecurityTests(unittest.TestCase):
    def setUp(self):
        self.profile = json.loads(
            (ROOT / "skills/job-search-jev/assets/profile.template.json").read_text()
        )
        self.profile["jev"]["enabled"] = True
        self.marker = secrets.token_hex(20)

    def test_ranking_request_drops_unexpected_private_fields(self):
        self.profile["salary"]["secret"] = self.marker
        self.profile["eligibility"]["private_note"] = self.marker
        self.profile["criteria"][0]["private_note"] = self.marker
        job = {
            "title": "Nurse",
            "description": "Public job duties",
            "employer_url": "https://example.org/?session=" + self.marker,
            "application_form": {"note": self.marker},
            "raw_html": self.marker,
            "evaluation": {"raw_response": self.marker},
            "salary": {
                "min": 40,
                "max": 50,
                "currency": "CAD",
                "period": "hour",
                "employer_reported": True,
                "cookie": self.marker,
            },
        }
        payload = request(self.profile, job)
        self.assertNotIn(self.marker, json.dumps(payload))
        self.assertEqual(payload["state"]["job"]["description"], "Public job duties")
        self.assertEqual(payload["state"]["job"]["salary"]["min"], 40)

    def test_extraction_drops_source_and_nested_private_metadata(self):
        evidence = collect(
            {
                "text": "Public base CAD 45–50 per hour",
                "cookies": self.marker,
                "url": "https://example.org/?session=" + self.marker,
            }
        )
        self.assertNotIn("cookies", evidence["source"])
        evidence["salary_candidates"][0]["private_note"] = self.marker
        payload = extraction_request(evidence, self.profile)
        self.assertNotIn(self.marker, json.dumps(payload))
        self.assertEqual(payload["state"]["listing"]["salary_candidates"][0]["min"], 45)

    def test_extraction_sends_only_candidates_exposed_in_questions(self):
        evidence = collect(
            {
                "text": "\n".join(
                    f"Base CAD {40 + i}–{50 + i} per hour for region {i}"
                    for i in range(10)
                )
            }
        )
        payload = extraction_request(evidence, self.profile)
        self.assertEqual(len(payload["state"]["listing"]["salary_candidates"]), 8)
        self.assertTrue(payload["state"]["listing"]["overflow"])

    def test_malformed_nested_payloads_fail_before_transfer(self):
        for job in (
            {"description": {"secret": self.marker}},
            {"evidence_excerpts": [{}]},
            {"salary": {"min": {"secret": self.marker}}},
        ):
            with self.assertRaises(ValueError):
                request(self.profile, job)
        evidence = collect({"text": "Base CAD 45–50 per hour"})
        for key, value in [("sha256", {}), ("location_spans", [{}]), ("overflow", {})]:
            changed = copy.deepcopy(evidence)
            changed[key] = value
            with self.assertRaises(ValueError):
                extraction_request(changed, self.profile)
        evidence["salary_candidates"][0]["min"] = {"secret": self.marker}
        with self.assertRaises(ValueError):
            extraction_request(evidence, self.profile)

    def test_installer_rejects_escaping_skill_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            (root / "skills").mkdir(parents=True)
            (root / "skills/job-search-jev").symlink_to(
                ROOT / "skills/job-search-jev", target_is_directory=True
            )
            destination = Path(tmp) / "install"
            with patch.object(install, "ROOT", root):
                with self.assertRaisesRegex(ValueError, "root escapes"):
                    install.install("codex", destination)
            self.assertFalse(destination.exists())

    def test_installer_preflights_missing_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            shutil.copytree(ROOT / "skills", root / "skills")
            (root / "skills/job-search-jev/LICENSE").unlink()
            destination = Path(tmp) / "install"
            with patch.object(install, "ROOT", root):
                with self.assertRaises(ValueError):
                    install.install("codex", destination)
            self.assertFalse(destination.exists())

    def test_supported_python_baseline(self):
        with patch.object(install.sys, "version_info", (3, 10, 0)):
            with self.assertRaisesRegex(ValueError, "3.11"):
                install.install("codex", "unused")

    def test_archive_write_preserves_hard_linked_victim(self):
        with tempfile.TemporaryDirectory() as tmp:
            victim = Path(tmp) / "keep.txt"
            victim.write_text("KEEP")
            archive = Path(tmp) / "out.zip"
            archive.hardlink_to(victim)
            package.pack(archive, [("README.md", "README.md")])
            self.assertEqual(victim.read_text(), "KEEP")
            with zipfile.ZipFile(archive) as z:
                self.assertIn("README.md", z.namelist())

    def test_atomic_text_output_preserves_hard_linked_victim(self):
        with tempfile.TemporaryDirectory() as tmp:
            victim = Path(tmp) / "keep.txt"
            victim.write_text("KEEP")
            output = Path(tmp) / "guide.md"
            output.hardlink_to(victim)
            package.atomic_write(output, b"new guide")
            self.assertEqual(victim.read_text(), "KEEP")
            self.assertEqual(output.read_text(), "new guide")

    def test_public_template_rejects_personalization(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "skills/job-search-jev/assets/profile.template.json"
            path.parent.mkdir(parents=True)
            original = json.loads(
                (
                    ROOT / "skills/job-search-jev/assets/profile.template.json"
                ).read_text()
            )
            variants = []
            for key, value in [
                ("candidate_evidence", [self.marker]),
                ("target_roles", ["Nurse"]),
                ("email", self.marker),
            ]:
                profile = copy.deepcopy(original)
                profile[key] = value
                variants.append(profile)
            profile = copy.deepcopy(original)
            profile["salary"]["minimum"] = 100
            variants.append(profile)
            profile = copy.deepcopy(original)
            profile["eligibility"]["residence"] = "Example"
            variants.append(profile)
            profile = copy.deepcopy(original)
            profile["jev"]["enabled"] = True
            variants.append(profile)
            for profile in variants:
                path.write_text(json.dumps(profile))
                with patch.object(package, "ROOT", root):
                    with self.assertRaises(ValueError):
                        package.validate_public_profile()

    def test_unsafe_or_missing_employer_links_never_qualify(self):
        for url in (
            "javascript:alert(1)",
            "file:///tmp/private",
            "https://user:pass@example.org/job",
            None,
            123,
        ):
            job = {
                "company": "Example",
                "requisition_id": "1",
                "employer_url": url,
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
            result = rank(self.profile, [job], [])
            self.assertEqual(result["shortlist"], [])
            self.assertIn(
                "employer_url_invalid_or_missing", result["review"][0]["reasons"]
            )

    def test_starter_sources_are_manual_by_default(self):
        sources = json.loads(
            (ROOT / "skills/job-search-jev/assets/sources.starter.json").read_text()
        )["sources"]
        self.assertTrue(sources)
        self.assertTrue(all(source["access_mode"] == "manual" for source in sources))

    def test_disabled_jev_blocks_both_payload_generators(self):
        self.profile["jev"]["enabled"] = False
        with self.assertRaises(ValueError):
            request(self.profile, {"title": "Nurse"})
        with self.assertRaises(ValueError):
            extraction_request(
                collect({"text": "Base CAD 45–50 per hour"}), self.profile
            )

    def test_source_access_mode_validation(self):
        self.profile["sources"] = [
            {
                "name": "Example",
                "url": "https://example.org",
                "kind": "board",
                "enabled": True,
                "access_mode": "bypass",
            }
        ]
        with self.assertRaises(ValueError):
            validate(self.profile)
        self.profile["sources"][0]["access_mode"] = "manual"
        validate(self.profile)


if __name__ == "__main__":
    unittest.main()
