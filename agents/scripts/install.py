"""Install the public skill locally without replacing an existing installation."""

import argparse
from pathlib import Path
import shutil
import sys
import tempfile
from package import SKILL_FILES

ROOT = Path(__file__).resolve().parents[1]


def install(host, skills_dir=None):
    if sys.version_info < (3, 11):
        raise ValueError("Use a supported Python release, version 3.11 or newer")
    if host not in ("claude-code", "codex"):
        raise ValueError("Host must be claude-code or codex")
    parent = (
        Path(skills_dir).expanduser()
        if skills_dir
        else Path.home()
        / {"claude-code": ".claude/skills", "codex": ".agents/skills"}[host]
    )
    source = ROOT / "skills/job-search-jev"
    if source.is_symlink() or not source.resolve().is_relative_to(ROOT.resolve()):
        raise ValueError("Skill root escapes the repository; refusing installation")
    target = parent / source.name
    if target.exists() or target.is_symlink():
        raise ValueError(
            f"{target} already exists. Review it before updating; nothing was replaced."
        )
    files = [source / name for name in SKILL_FILES]
    if any(
        not p.is_file()
        or p.is_symlink()
        or not p.resolve().is_relative_to(source.resolve())
        for p in files
    ):
        raise ValueError("Skill contains an unsafe package path; refusing installation")
    if not (source / "SKILL.md").is_file():
        raise ValueError("Missing SKILL.md")
    parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".jobscout-", dir=parent) as staging:
        ready = Path(staging) / source.name
        for path in files:
            dest = ready / path.relative_to(source)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, dest)
        ready.rename(target)
    return target


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", required=True, choices=("claude-code", "codex"))
    parser.add_argument("--skills-dir", help="Override the host skill directory")
    args = parser.parse_args()
    try:
        print(
            f"Installed JobScout at {install(args.host, args.skills_dir)}. Start a new chat, then ask to configure JobScout."
        )
    except (OSError, ValueError) as error:
        parser.exit(2, str(error) + "\n")
