# Installation checks

These checks record observed installation behavior. They do not establish that a hosted conversation, source retrieval, or JEV evaluation works.

[Environment](#environment) · [Results](#results) · [Limits](#limits) · [Reproduce](#reproduce)

## Environment

- Date: November 18, 2026
- Host: macOS
- Claude Code: 2.1.326
- JobScout marketplace package: 0.2.2 from the public default branch
- Local installer: the 0.2.2 source in this repository
- Isolation: temporary Claude configuration and separate temporary skill directories

The checks did not change existing user installations, configure a candidate profile, or connect JEV.

## Results

| Route or check | Observed result |
| --- | --- |
| `claude plugin install jobscout --marketplace mlohmann/ai-skills --json` | Exit 0; installed `jobscout@ai-skills` |
| `claude plugin list --json` | Exit 0; listed JobScout 0.2.2 as enabled |
| Marketplace-installed skill | `skills/job-search-jev/SKILL.md` existed in the isolated installation |
| Local installer with `--host codex --skills-dir PATH` | Exit 0; installed files matched source bytes |
| Local installer with `--host claude-code --skills-dir PATH` | Exit 0; installed files matched source bytes |
| Repeat local installation at the same destination | Exit 2; refused to replace the existing skill |

The two local installer checks used explicit destination overrides. They did not test host discovery in a new Codex or Claude conversation or installation into the default user directories. An enabled Claude plugin is not JEV authorization.

## Limits

These checks did not verify:

- Skill discovery and profile setup in a new conversation
- Claude.ai skill upload or ChatGPT Project setup
- Interactive `/plugin` installation
- Installation on Windows or Linux
- Live job-source retrieval, mail access, or spreadsheet writes
- Authenticated JEV calls, provider response normalization, or cost savings

Use the [host acceptance checklist](acceptance.md) for these separate checks. Do not describe them as tested on the basis of a successful file installation.

## Reproduce

Use the [installation guide](../INSTALL.md). For the marketplace check, run the documented shell command, then `claude plugin list`. A separate temporary `CLAUDE_CONFIG_DIR` can isolate this check from an existing Claude installation.

For the local installer, select an empty temporary directory with `--skills-dir PATH`. Compare the installed files with `skills/job-search-jev/`, then run the command again and confirm that it refuses to replace the installation.

Claude documents marketplace installation in [Install and manage plugins](https://code.claude.com/docs/en/discover-plugins). The command help on the tested client also confirmed the `--marketplace` option. Support in other client versions was not tested.
