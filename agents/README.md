# JobScout

A configurable job-search skill for ChatGPT and Claude. Bring your own profile, choose job sources, and get an evidence-backed shortlist with an explicit review queue. Any occupation; JEV is optional and off by default.

## Start with one instruction

Paste this into your AI agent:

> Read https://raw.githubusercontent.com/mlohmann/ai-skills/main/agents/INSTALL.md and install JobScout for this environment. Help me create my private profile and choose a starter source board or my own sources. Leave JEV off unless I opt in.

Claude Code also supports a single shell command (2.1.275+; available after merge):

```sh
claude plugin install jobscout --marketplace mlohmann/ai-skills
```

[Installation guide](INSTALL.md) · [ChatGPT](chatgpt/setup.md) · [Claude](claude/setup.md)

Claude Code and Codex have a local installer. Claude.ai has an uploadable skill ZIP. ChatGPT has a portable skill plugin for supported hosts and a private Project kit. The agent guides any account-specific upload steps; an instruction cannot grant new tools or permissions.

## Make it yours

Fill out your profile in conversation or use [the form](skills/job-search-jev/assets/profile-form.md). Set roles, location/authorization, work model, supported experience, pay rules, exclusions and ranking priorities. No résumé is required. Keep the completed profile private.

Start with [the source list](skills/job-search-jev/assets/sources.starter.json), a [blank source board](skills/job-search-jev/assets/sources.blank.json), or your own employer pages, saved searches and specialty boards. The starter includes Indeed and LinkedIn as enabled manual discovery links; optional Idealist and We Work Remotely entries can be enabled when relevant. All starter sources are manual by default. Automated retrieval needs provider permission for the specific method; a login is insufficient. Sources are configurable discovery links, not bundled crawler integrations. Every source can be removed or replaced.

Keep results in a private Markdown board or use [the CSV template](skills/job-search-jev/assets/listings-board.csv). The board is a file you control, not a hosted web app.

Assistant review works without JEV. Opt into JEV for structured evaluation using your own supported connection, with optional fallback or a required-evaluator setting. Both modes apply the same salary, eligibility, freshness, deduplication and application-history rules. Scores never override hard gates. Unknowns remain reviewable; no invented candidate claims or evaluator confidence.

## Downloads

Version 0.2.0 packages are in [releases/0.2.0](releases/0.2.0/):

- `jobscout-0.2.0-source.zip`: full public source kit, installation instructions and tests.
- `jobscout-chatgpt-plugin.zip`: portable Agent Plugin layout.
- `job-search-jev-claude.zip`: uploadable Claude skill.
- `jobscout-claude-code-plugin.zip`: Claude Code plugin layout.
- `SHA256SUMS`: archive integrity checksums.

The source kit includes `chatgpt/jobscout-guide.md`, a consolidated Project reference. Prebuilt archives are generated from an explicit public-file allowlist; user profiles, run artifacts, local caches, Git history and credentials are excluded.

## Verify or rebuild

Python 3.11+; no third-party Python dependencies.

```sh
cd agents
python3 -m unittest discover -s tests -v
python3 scripts/package.py
```

The installer refuses to replace an existing installation. Runtime profiles/results belong in a private workspace outside this repository. No applications, outreach, uploads, account creation or scheduling happen as part of a search.

See [the host acceptance checks](tests/acceptance.md) for remaining verification. A successful local build is not proof of ChatGPT web installation, Claude.ai installation, live source coverage or JEV inference. Public plugin-directory acceptance is separate from this repository release. Source/download URLs are live after the release lands on the default branch.

JobScout under `agents/` is MIT licensed: [LICENSE](LICENSE). JEV and host services are separate products with their own terms, access and potential costs. This license does not change the licensing of unrelated repository content.

## Security and privacy

Read [SECURITY.md](SECURITY.md) and [PRIVACY.md](PRIVACY.md) before public rollout. These describe real data flows and review limits; this package makes no GDPR, SOC 2, security-certification or platform-approval claim. The public license applies to JobScout code/instructions, not third-party content or services.
