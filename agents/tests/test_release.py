import copy
from datetime import date
import hashlib
import json
import re
from pathlib import Path
import shutil
import secrets
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/job-search-jev/scripts"))
sys.path.insert(0, str(ROOT / "scripts"))
from jobscout import identity, rank, request, validate
from evidence import collect, extraction_request, resolve
import package
import install


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.p = json.loads(
            (ROOT / "skills/job-search-jev/assets/profile.template.json").read_text()
        )
        self.j = dict(
            company="Example",
            requisition_id="1",
            title="Nurse",
            location="Toronto",
            employer_url="https://example.org/jobs?id=1",
            role_eligible=True,
            seniority_eligible=True,
            location_eligible=True,
            work_model_eligible=True,
            active=True,
            employer_verified=True,
            evaluation=dict(
                provider="assistant",
                confidence=None,
                scores={c["id"]: 80 for c in self.p["criteria"]},
            ),
        )

    def test_default_assistant_qualifies_without_confidence(self):
        validate(self.p)
        result = rank(self.p, [self.j], [])
        self.assertEqual(result["shortlist"][0]["provider"], "assistant")
        self.assertEqual(result["shortlist"][0]["score"], 80)
        self.assertIsNone(result["shortlist"][0]["job"]["evaluation"]["confidence"])
        with self.assertRaisesRegex(ValueError, "disabled"):
            request(self.p, self.j)

    def test_jev_fallback_required_and_disabled(self):
        self.p["jev"].update(enabled=True, required=False)
        self.assertEqual(len(rank(self.p, [self.j], [])["shortlist"]), 1)
        self.p["jev"]["required"] = True
        self.assertIn(
            "jev_required", rank(self.p, [self.j], [])["review"][0]["reasons"]
        )
        self.p["jev"]["enabled"] = False
        with self.assertRaises(ValueError):
            validate(self.p)

    def test_both_providers_obey_gates_and_missing_history(self):
        for provider in ("assistant", "jev"):
            self.j["evaluation"].update(provider=provider, confidence=0.95)
            self.j["location_eligible"] = False
            self.assertEqual(len(rank(self.p, [self.j], [])["excluded"]), 1)
            self.j["location_eligible"] = None
            self.assertEqual(len(rank(self.p, [self.j], [])["review"]), 1)
            self.j["location_eligible"] = True
            self.assertEqual(len(rank(self.p, [self.j])["review"]), 1)

    def test_history_url_can_match_id_bearing_job(self):
        history = [
            dict(
                company="Example",
                employer_url="https://example.org/jobs?id=1&utm_source=mail",
                status="applied",
            )
        ]
        self.assertIn(
            "application_history",
            rank(self.p, [self.j], history)["excluded"][0]["reasons"],
        )

    def test_distinct_query_ids_stay_distinct(self):
        one = dict(employer_url="https://example.org/job?jobId=1&utm_source=mail")
        two = dict(employer_url="https://example.org/job?jobId=2")
        self.assertNotEqual(identity(one), identity(two))
        self.assertEqual(
            identity(one),
            identity(dict(employer_url="https://example.org/job?jobId=1#section")),
        )

    def test_duplicate_aliases_require_consolidation(self):
        other = copy.deepcopy(self.j)
        other.pop("requisition_id")
        out = rank(self.p, [self.j, other], [])
        self.assertEqual(out["duplicate_count"], 1)
        self.assertEqual(len(out["review"]), 1)
        self.assertEqual(out["shortlist"], [])

    def test_distinct_explicit_requisitions_remain_eligible(self):
        other = copy.deepcopy(self.j)
        other["requisition_id"] = "2"
        self.assertEqual(len(rank(self.p, [self.j, other], [])["shortlist"]), 2)
        self.assertEqual(
            len(rank(self.p, [self.j], [dict(other, status="applied")])["shortlist"]), 1
        )

    def test_pay_matches_currency_and_period(self):
        self.p["salary"].update(minimum=40, currency="CAD", period="hour")
        self.j["salary"] = dict(
            min=40, max=50, currency="CAD", period="hour", employer_reported=True
        )
        self.assertEqual(len(rank(self.p, [self.j], [])["shortlist"]), 1)
        for key, value in [
            ("currency", "USD"),
            ("period", "year"),
            ("employer_reported", False),
        ]:
            job = copy.deepcopy(self.j)
            job["salary"][key] = value
            self.assertEqual(len(rank(self.p, [job], [])["review"]), 1)

    def test_freshness(self):
        self.p["max_age_days"] = 7
        for posted, bucket in [
            ("2026-11-01", "excluded"),
            ("2026-11-16", "review"),
            (None, "review"),
            ("2026-11-15", "shortlist"),
        ]:
            self.j["posted_at"] = posted
            self.assertEqual(
                len(rank(self.p, [self.j], [], today=date(2026, 11, 15))[bucket]), 1
            )

    def test_invalid_profiles_fail_cleanly(self):
        for key, value in [
            ("version", True),
            ("criteria", [None]),
            ("criteria", [{"id": []}]),
            ("salary", None),
            ("jev", None),
            ("sources", [{"url": 12}]),
            ("target_roles", [{}]),
            ("sources", [{"name": "Bad", "url": "file:///private", "kind": "board"}]),
            ("preferences", {}),
            ("eligibility", {}),
        ]:
            with self.subTest(key=key, value=value):
                p = copy.deepcopy(self.p)
                p[key] = value
                with self.assertRaises(ValueError):
                    validate(p)
        self.p["salary"]["minimum"] = 100
        with self.assertRaises(ValueError):
            validate(self.p)

    def test_missing_or_malformed_evaluation_is_review(self):
        for ev in (
            None,
            "bad",
            {"provider": "assistant", "scores": []},
            {
                "provider": "invented",
                "scores": {c["id"]: 80 for c in self.p["criteria"]},
            },
        ):
            self.j["evaluation"] = ev
            self.assertEqual(len(rank(self.p, [self.j], [])["review"]), 1)

    def test_request_omits_private_source_configuration(self):
        self.p["jev"]["enabled"] = True
        self.p["sources"] = ["https://private.example/search"]
        context = request(self.p, self.j)["state"]["profile"]
        self.assertNotIn("sources", context)
        self.assertNotIn("jev", context)

    def test_nonsoftware_non_us_extraction(self):
        self.p["jev"]["enabled"] = True
        self.p["target_roles"] = ["Nurse"]
        self.p["locations"] = ["Toronto, Canada"]
        self.p["salary"].update(currency="CAD", period="hour")
        e = collect({"text": "Location: Toronto\nBase pay CAD 45.50–55.75 per hour"})
        payload = extraction_request(e, self.p)
        self.assertEqual(payload["state"]["target"]["target_roles"], ["Nurse"])
        self.assertEqual(payload["state"]["target"]["locations"], ["Toronto, Canada"])
        self.assertNotIn("Washington", json.dumps(payload))
        self.assertNotIn("frontend", json.dumps(payload))
        self.assertEqual(e["salary_candidates"][0]["min"], 45.5)
        self.assertEqual(e["salary_candidates"][0]["currency"], "CAD")

    def test_exact_values_offsets_hash_and_form_cutoff(self):
        e = collect(
            {
                "text": "<div>Base USD 125,400–187,650 per year</div><div>Apply for this job</div><p>Expected USD 300,000–400,000</p>"
            }
        )
        self.assertEqual(len(e["salary_candidates"]), 1)
        c = e["salary_candidates"][0]
        self.assertEqual((c["min"], c["max"]), (125400, 187650))
        self.assertEqual(
            e["text"][c["offset"] :][: len(c["range_text"])], c["range_text"]
        )
        self.assertEqual(e["sha256"], hashlib.sha256(e["text"].encode()).hexdigest())

    def test_ambiguous_formats_and_currency(self):
        self.assertIsNone(
            collect({"text": "Base $60k–$80k"})["salary_candidates"][0]["currency"]
        )
        self.assertEqual(
            collect({"text": "Base €60.000–80.000"})["salary_candidates"], []
        )
        self.assertEqual(
            collect({"text": "Base €60,000–80,000"})["salary_candidates"][0][
                "currency"
            ],
            "EUR",
        )

    def test_invalid_confidence_and_choices_are_review(self):
        e = collect({"text": "Base USD 60k–80k per year"})
        for confidence in (True, float("nan"), float("inf"), 1.1, None, 0.2):
            answers = {
                n: {"choice": "eligible", "confidence": confidence}
                for n in ("role_scope", "seniority", "location")
            }
            answers["salary_evidence"] = {"choice": "pay_0", "confidence": confidence}
            self.assertTrue(resolve(e, {"answers": answers})["review_reasons"])
        bad = resolve(
            e, {"answers": {"salary_evidence": {"choice": "pay_999", "confidence": 1}}}
        )
        self.assertIsNone(bad["selected_salary"])
        self.assertIn("salary_evidence_answer_invalid", bad["review_reasons"])
        self.assertTrue(
            resolve(e, {"answers": {"salary_evidence": None}})["review_reasons"]
        )

    def test_mixed_currency_and_invalid_answer_shapes_are_review(self):
        evidence = collect({"text": "Base $60k–€80k"})
        self.assertIsNone(evidence["salary_candidates"][0]["currency"])
        self.assertTrue(evidence["salary_candidates"][0]["currency_conflict"])
        self.assertTrue(
            resolve(
                evidence,
                {"answers": {"salary_evidence": {"choice": [], "confidence": 1}}},
            )["review_reasons"]
        )

    def test_package_output_symlinks_do_not_overwrite_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            safe = Path(tmp) / "keep.txt"
            safe.write_text("KEEP")
            (Path(tmp) / "jobscout-chatgpt-plugin.zip").symlink_to(safe)
            with self.assertRaises(ValueError):
                package.build(tmp)
            self.assertEqual(safe.read_text(), "KEEP")

    def test_guide_output_symlinks_do_not_overwrite_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            isolated = Path(tmp) / "source"
            for rel in package.PUBLIC_FILES:
                dest = isolated / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / rel, dest)
            safe = Path(tmp) / "keep.txt"
            safe.write_text("KEEP")
            guide = isolated / "chatgpt/jobscout-guide.md"
            guide.unlink()
            guide.symlink_to(safe)
            with patch.object(package, "ROOT", isolated):
                with self.assertRaises(ValueError):
                    package.build(Path(tmp) / "dist")
            self.assertEqual(safe.read_text(), "KEEP")

    def test_starter_sources_validate(self):
        board = json.loads(
            (ROOT / "skills/job-search-jev/assets/sources.starter.json").read_text()
        )
        self.p["sources"] = board["sources"]
        validate(self.p)
        self.assertEqual(sum(s["enabled"] for s in board["sources"]), 2)

    def test_cli_invalid_json_has_no_traceback(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            path.write_text("{broken")
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "skills/job-search-jev/scripts/jobscout.py"),
                    "validate",
                    str(path),
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 2)
            self.assertNotIn("Traceback", result.stderr)

    def test_installer_public_files_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = install.install("claude-code", tmp)
            self.assertTrue((target / "SKILL.md").is_file())
            before = (target / "SKILL.md").read_bytes()
            with self.assertRaisesRegex(ValueError, "already exists"):
                install.install("claude-code", tmp)
            self.assertEqual((target / "SKILL.md").read_bytes(), before)
            self.assertEqual(
                sorted(
                    str(p.relative_to(target)) for p in target.rglob("*") if p.is_file()
                ),
                sorted(package.SKILL_FILES),
            )

    def test_installer_broken_symlink_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "job-search-jev").symlink_to(Path(tmp) / "missing")
            with self.assertRaises(ValueError):
                install.install("codex", tmp)

    def test_project_guide_navigation_and_reference_links(self):
        with tempfile.TemporaryDirectory() as tmp:
            package.build(tmp)
        guide = (ROOT / "chatgpt/jobscout-guide.md").read_text(encoding="utf-8")
        headings = re.findall(r"^#{1,6} (.+)$", guide, flags=re.MULTILINE)
        anchors = {
            re.sub(r"[^\w\s-]", "", heading.lower()).replace(" ", "-")
            for heading in headings
        }
        for target in re.findall(r"\]\(([^\s)]+)\)", guide):
            if target.startswith("#"):
                self.assertIn(target[1:], anchors)
            elif not target.startswith(("https://", "http://")):
                self.assertTrue(
                    (ROOT / "chatgpt" / target.split("#")[0]).exists(), target
                )
        self.assertIn(
            "https://github.com/mlohmann/ai-skills/blob/main/agents/skills/job-search-jev/assets/profile.template.json",
            guide,
        )

        for name in (
            "profile.template.json",
            "sources.blank.json",
            "sources.starter.json",
        ):
            template = (ROOT / "skills/job-search-jev/assets" / name).read_text(
                encoding="utf-8"
            )
            self.assertIn("```json\n" + template + "```", guide)

    def test_reproducible_archives_checksums_and_layouts(self):
        with tempfile.TemporaryDirectory() as tmp:
            names = package.build(tmp)
            before = {n: (Path(tmp) / n).read_bytes() for n in names}
            package.build(tmp)
            for name in names:
                self.assertEqual(before[name], (Path(tmp) / name).read_bytes())
                with zipfile.ZipFile(Path(tmp) / name) as z:
                    paths = z.namelist()
                    self.assertTrue(
                        all(
                            "__pycache__" not in p
                            and not p.endswith(".pyc")
                            and ".git/" not in p
                            and "private/" not in p
                            for p in paths
                        )
                    )
                    self.assertTrue(
                        all(("/" + "Users/") not in z.read(p).decode() for p in paths)
                    )
                    self.assertTrue(
                        all(
                            not p.startswith("/") and ".." not in Path(p).parts
                            for p in paths
                        )
                    )
                    if name == "job-search-jev-claude.zip":
                        self.assertIn("job-search-jev/SKILL.md", paths)
                    if name == "jobscout-chatgpt-plugin.zip":
                        self.assertIn("plugin.json", paths)
                    if name == "jobscout-claude-code-plugin.zip":
                        self.assertIn(".claude-plugin/plugin.json", paths)
            sums = (Path(tmp) / "SHA256SUMS").read_text().splitlines()
            self.assertEqual(len(sums), 4)
            for line in sums:
                checksum, name = line.split("  ")
                self.assertEqual(
                    checksum,
                    hashlib.sha256((Path(tmp) / name).read_bytes()).hexdigest(),
                )

    def test_private_injection_excluded_and_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            isolated = Path(tmp) / "source"
            for rel in package.PUBLIC_FILES:
                dest = isolated / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / rel, dest)
            marker = secrets.token_hex(16)
            (isolated / "skills/job-search-jev/assets/private-profile.json").write_text(
                marker
            )
            (isolated / ".env").write_text(marker)
            with patch.object(package, "ROOT", isolated):
                names = package.build(Path(tmp) / "dist")
                for name in names:
                    with zipfile.ZipFile(Path(tmp) / "dist" / name) as z:
                        self.assertTrue(
                            all(marker.encode() not in z.read(p) for p in z.namelist())
                        )
                (isolated / "LICENSE").unlink()
                (isolated / "LICENSE").symlink_to(ROOT / "LICENSE")
                with self.assertRaises(ValueError):
                    package.build(Path(tmp) / "unsafe")


if __name__ == "__main__":
    unittest.main()
