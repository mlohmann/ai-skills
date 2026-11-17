"""Build packages from named public files. Do not include private profiles."""

from pathlib import Path
import hashlib
import io
import json
import os
import re
import tempfile
import zipfile
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[1]
SKILL_FILES = [
    "SKILL.md",
    "LICENSE",
    "assets/profile.template.json",
    "assets/profile-form.md",
    "assets/sources.blank.json",
    "assets/sources.starter.json",
    "assets/listings-board.csv",
    "references/workflow.md",
    "references/jev.md",
    "references/data-contract.md",
    "references/extraction.md",
    "references/sources.md",
    "references/privacy.md",
    "scripts/evidence.py",
    "scripts/jobscout.py",
    "scripts/evaluation_cache.py",
]
SKILL_PREFIX = "skills/job-search-jev/"
PUBLIC_FILES = [
    "README.md",
    "INSTALL.md",
    "LICENSE",
    ".gitignore",
    "plugin.json",
    ".claude-plugin/plugin.json",
    ".agents/plugins/marketplace.json",
    "chatgpt/setup.md",
    "chatgpt/instructions.md",
    "chatgpt/jobscout-guide.md",
    "claude/setup.md",
    "claude/project-instructions.md",
    "scripts/package.py",
    "scripts/install.py",
    "tests/test_jobscout.py",
    "tests/test_release.py",
    "tests/acceptance.md",
    "SECURITY.md",
    "PRIVACY.md",
    "tests/test_security.py",
    "tests/test_regressions.py",
    "tests/test_duplicates.py",
    "tests/test_evaluation_cache.py",
] + [SKILL_PREFIX + p for p in SKILL_FILES]


def atomic_write(path, data):
    """Replace the output entry. Do not write through an existing hard link."""
    if path.is_symlink():
        raise ValueError("Refusing a symbolic-link output destination")
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            dir=path.parent, prefix=".jobscout-", delete=False
        ) as output:
            temporary = Path(output.name)
            output.write(data)
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def validate_public_profile():
    template = ROOT / "skills/job-search-jev/assets/profile.template.json"
    if template.is_symlink() or not template.resolve().is_relative_to(ROOT.resolve()):
        raise ValueError("Unsafe public profile template")
    profile = json.loads(template.read_text(encoding="utf-8"))
    empty_lists = (
        "target_roles",
        "seniority",
        "locations",
        "work_models",
        "excluded_companies",
        "candidate_evidence",
        "sources",
        "preferences",
    )
    allowed = set(empty_lists) | {
        "version",
        "salary",
        "exclude_history_statuses",
        "criteria",
        "top_n",
        "min_fit",
        "min_confidence",
        "jev",
        "max_age_days",
        "eligibility",
    }
    if (
        not isinstance(profile, dict)
        or set(profile) != allowed
        or any(profile.get(k) != [] for k in empty_lists)
    ):
        raise ValueError(
            "Public profile must be blank; save personal profiles outside the repository"
        )
    if profile.get("eligibility") != {
        "residence": None,
        "authorized_countries": [],
        "requires_sponsorship": None,
    }:
        raise ValueError("Public profile contains personal eligibility settings")
    salary = profile.get("salary")
    if (
        not isinstance(salary, dict)
        or set(salary) != {"minimum", "currency", "period", "gate", "missing"}
        or salary["minimum"] is not None
        or salary["currency"] is not None
    ):
        raise ValueError("Public salary template must be unconfigured")
    if not isinstance(profile.get("criteria"), list) or any(
        not isinstance(c, dict) or set(c) != {"id", "description", "weight"}
        for c in profile["criteria"]
    ):
        raise ValueError("Unexpected public criterion metadata")
    if (
        not isinstance(profile.get("jev"), dict)
        or profile["jev"].get("enabled") is not False
        or profile["jev"].get("required") is not False
    ):
        raise ValueError("Public template must leave JEV disabled")


def pack(path, entries):
    if path.is_symlink():
        raise ValueError("Refusing a symbolic-link archive destination")
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
        for relative, archive_name in entries:
            source = ROOT / relative
            if source.is_symlink() or not source.resolve().is_relative_to(
                ROOT.resolve()
            ):
                raise ValueError("Refusing an escaping package path: " + relative)
            data = source.read_bytes()
            # Use fixed metadata so identical input produces identical archives.
            info = zipfile.ZipInfo(archive_name, (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    atomic_write(path, buffer.getvalue())


def build(dist=None):
    validate_public_profile()
    guide_parts = [
        "skills/job-search-jev/SKILL.md",
        "skills/job-search-jev/assets/profile-form.md",
        "skills/job-search-jev/references/workflow.md",
        "skills/job-search-jev/references/sources.md",
        "skills/job-search-jev/references/data-contract.md",
        "skills/job-search-jev/references/jev.md",
        "skills/job-search-jev/references/extraction.md",
        "skills/job-search-jev/references/privacy.md",
        "skills/job-search-jev/assets/profile.template.json",
        "skills/job-search-jev/assets/sources.blank.json",
        "skills/job-search-jev/assets/sources.starter.json",
        "skills/job-search-jev/assets/listings-board.csv",
    ]
    parts = [
        "# JobScout Project guide\n\nUse this reference with ChatGPT or Claude Project instructions. Each section includes the source file content. You do not need to upload those files separately. Use the helper commands only if the scripts and code execution are available.\n\n[Profile form](#your-jobscout-profile) · [Workflow](#jobscout-workflow) · [Source and results boards](#source-boards-and-results-boards) · [Helper reference](#offline-helper-reference) · [JEV](#jev-integration) · [Extraction](#evidence-extraction) · [Privacy](#privacy-and-external-services)\n"
    ]
    for relative in guide_parts:
        source = ROOT / relative
        if source.is_symlink() or not source.resolve().is_relative_to(ROOT.resolve()):
            raise ValueError("Unsafe guide source: " + relative)
        body = source.read_text(encoding="utf-8")
        if source.suffix == ".md":
            # Keep one navigation index in the combined guide.
            body = (
                "\n".join(
                    line
                    for line in body.splitlines()
                    if not (line.startswith("[") and "](#" in line and " · " in line)
                )
                + "\n"
            )
            # Resolve source links for readers who have only the combined guide.
            base_url = (
                "https://github.com/mlohmann/ai-skills/blob/main/agents/" + relative
            )
            body = re.sub(
                r"(?<=\]\()([^\s)]+)(?=\))",
                lambda match: match.group(1)
                if match.group(1).startswith("#")
                else urljoin(base_url, match.group(1)),
                body,
            )
        parts.append(
            "\n---\n\n## "
            + relative
            + "\n\n"
            + (
                "```json\n" + body + "```\n"
                if source.suffix == ".json"
                else "```csv\n" + body + "```\n"
                if source.suffix == ".csv"
                else body
            )
        )
    guide = ROOT / "chatgpt/jobscout-guide.md"
    if guide.is_symlink() or not guide.resolve().is_relative_to(ROOT.resolve()):
        raise ValueError("Unsafe guide destination")
    atomic_write(guide, "\n".join(parts).encode("utf-8"))
    if dist is None and not (ROOT / "releases/0.2.2").resolve().is_relative_to(
        ROOT.resolve()
    ):
        raise ValueError("Unsafe release destination")
    dist = Path(dist) if dist else ROOT / "releases/0.2.2"
    dist.mkdir(parents=True, exist_ok=True)
    # Check all public files before writing a release archive.
    for relative in PUBLIC_FILES:
        path = ROOT / relative
        if (
            not path.is_file()
            or path.is_symlink()
            or not path.resolve().is_relative_to(ROOT.resolve())
        ):
            raise ValueError("Missing or unsafe public file: " + relative)
    packages = {
        "jobscout-0.2.2-source.zip": [(p, "jobscout/" + p) for p in PUBLIC_FILES],
        "jobscout-chatgpt-plugin.zip": [
            ("plugin.json", "plugin.json"),
            ("LICENSE", "LICENSE"),
        ]
        + [(SKILL_PREFIX + p, SKILL_PREFIX + p) for p in SKILL_FILES],
        "job-search-jev-claude.zip": [
            (SKILL_PREFIX + p, "job-search-jev/" + p) for p in SKILL_FILES
        ],
        "jobscout-claude-code-plugin.zip": [
            (".claude-plugin/plugin.json", ".claude-plugin/plugin.json"),
            ("LICENSE", "LICENSE"),
        ]
        + [(SKILL_PREFIX + p, SKILL_PREFIX + p) for p in SKILL_FILES],
    }
    if any((dist / name).is_symlink() for name in [*packages, "SHA256SUMS"]):
        raise ValueError("Refusing a symbolic-link release destination")
    for name, entries in packages.items():
        pack(dist / name, entries)
    checksums = "".join(
        hashlib.sha256((dist / name).read_bytes()).hexdigest() + "  " + name + "\n"
        for name in sorted(packages)
    )
    atomic_write(dist / "SHA256SUMS", checksums.encode("utf-8"))
    return list(packages)


if __name__ == "__main__":
    print("\n".join(build()))
