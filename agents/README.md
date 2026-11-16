# JobScout skills repository

Configurable job-search agents for ChatGPT and Claude. JEV evaluates role/skills/preferences; deterministic rules handle exclusions and weighted ranking. No occupation, location, salary floor or employer blacklist is hardcoded as a user's preference.

## Start
- ChatGPT: [setup](chatgpt/setup.md), instruction package and portable Agent Plugin.
- Claude: [setup](claude/setup.md), uploadable skill ZIP and Project instructions.
- Configure from [profile template](skills/job-search-jev/assets/profile.template.json), or tell the agent your preferences.

## Shared core
`skills/job-search-jev/` contains workflow, real discovered JEV request contract, configurable profile and standard-library Python helpers. Sources are supplied per user or discovered by the host agent. Mailbox/history access is optional and user-specific. Skills use tools supplied by the host; they are not standalone crawlers or scheduled services.

## Verify/build
```sh
python3 -m unittest discover -s tests -v
python3 scripts/package.py
```
Generated ZIPs: `dist/job-search-jev-claude.zip` (skill) and `dist/jobscout-chatgpt-plugin.zip` (portable plugin). Both exclude Git history, personal files and credentials. Share these packages or Git source; each recipient authenticates independently. Git repository initialized locally, no remote publication implied. No license is selected; ask the repository owner before redistribution beyond authorized sharing.

Status: authored and local deterministic tests verified; JEV input schema discovered, but no authenticated inference or installation/live search in either host was tested. Follow setup smoke tests in tests/acceptance.md before calling the agent live.
