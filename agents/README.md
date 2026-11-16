# JobScout

Find jobs with a search profile you control. JobScout brings profile setup, job sources, and results to ChatGPT and Claude. You can use it for any occupation. JEV, an optional evaluation service, is off by default.

[Get started](#get-started) · [Set up your search](#set-up-your-search) · [Downloads](#downloads) · [Build and test](#build-and-test) · [Privacy and security](#privacy-and-security)

## Get started

Paste this instruction into your AI agent:

> Read https://raw.githubusercontent.com/mlohmann/ai-skills/main/agents/INSTALL.md and install JobScout for this environment. Help me create my private profile and choose a starter source board or my own sources. Leave JEV off unless I opt in.

For Claude Code 2.1.275 or later, you can also use this command:

```sh
claude plugin install jobscout --marketplace mlohmann/ai-skills
```

These links and the marketplace command work after the release is merged into the default branch. Your host might require you to upload files or complete other setup steps.

Choose the guide for your host:

- [ChatGPT setup](chatgpt/setup.md)
- [Claude setup](claude/setup.md)
- [Installation guide for agents](INSTALL.md)

## Set up your search

### Create your profile

Answer questions in chat or fill out [the profile form](skills/job-search-jev/assets/profile-form.md). Set your target roles, location, work authorization, work model, and minimum base pay. Add experience you can support with examples. You don't need a résumé.

Keep your completed profile in a private location outside the installed skill and shared repository.

### Choose your sources

Start with [the source list](skills/job-search-jev/assets/sources.starter.json), use [a blank source board](skills/job-search-jev/assets/sources.blank.json), or add your own links.

A source board is a list of places to find jobs. The starter list includes Indeed and LinkedIn. You can also enable entries for Idealist and We Work Remotely. All starter entries are manual links for you to open. Automated retrieval requires the provider's permission for the method you use. Signing in doesn't grant that permission.

### Review your results

JobScout checks your required filters before it ranks fit. It keeps missing or conflicting facts in a review queue. An assistant fit score is a judgment, not a hiring probability.

Save results in a Markdown table or use [the CSV template](skills/job-search-jev/assets/listings-board.csv). This results board is a file you control. Saving a job doesn't submit an application.

### Use JEV if you want to

Assistant review works without JEV. To use JEV, connect your own supported service and choose whether assistant fallback is allowed. The host must explain what data it will send before your first JEV evaluation.

## Downloads

Choose a package in [releases/0.2.0](https://github.com/mlohmann/ai-skills/tree/main/agents/releases/0.2.0):

| File | Use |
| --- | --- |
| `jobscout-0.2.0-source.zip` | Source files, setup guides, templates, and tests |
| `jobscout-chatgpt-plugin.zip` | Portable Agent Plugin for supported hosts |
| `job-search-jev-claude.zip` | Skill upload for Claude.ai |
| `jobscout-claude-code-plugin.zip` | Plugin folder for Claude Code |
| `SHA256SUMS` | Checksums for the four archives |

The source kit includes `chatgpt/jobscout-guide.md`. Attach this file when you use the Project setup instructions. The build includes only files on its public-file list. Review their contents before you publish; the list doesn't detect every secret in allowed text.

## Build and test

Use Python 3.11 or later. The helpers use the Python standard library and modules in this package.

From the cloned repository root, run:

```sh
cd agents
python3 -m unittest discover -s tests -v
python3 scripts/package.py
```

If you extracted the source kit, run the last two commands from its `jobscout` folder. The build updates the Project guide, release archives, and checksums.

The local installer stops if the skill already exists. Review that installation before you update it. Keep generated review reports in the ignored `reports/` folder.

## Privacy and security

Read [the privacy guide](PRIVACY.md), [the security policy](SECURITY.md), and [the host acceptance checks](tests/acceptance.md). Local tests do not verify hosted-app installation, live source retrieval, or JEV inference. Platform directory submission is a separate step.

JEV off does not mean local-only AI processing. ChatGPT, Claude, and connected services use their own data settings and terms. JobScout does not apply for jobs, send messages, upload résumés, create accounts, or schedule searches as part of a scan.

JobScout under `agents/` uses the [MIT license](LICENSE). This license covers JobScout code and instructions. It doesn't grant rights to third-party content, brands, or services, or change the license of unrelated repository content. This package makes no regulatory certification or platform-approval claim.
