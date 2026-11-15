# Install JobScout

Give your AI agent this one instruction:

> Read https://raw.githubusercontent.com/mlohmann/ai-skills/main/agents/INSTALL.md and install JobScout for this environment. Help me create my private profile and choose a starter source board or my own sources. Leave JEV off unless I opt in.

This is an agent instruction, not a universal shell command. Your host's permissions, installed tools and workspace policies still apply. The files below become available on the default branch when the release is merged.

## Instructions for the installing agent

Identify the host before installing. This package needs no JEV account in its default mode. Never import the author's preferences or connect another service automatically. Install only the public JobScout files, not unrelated skills from the repository. Read `skills/job-search-jev/SKILL.md` after installation and run conversational onboarding; do not search until the current user confirms the profile.

### Claude Code: one-command plugin installation

On Claude Code 2.1.275 or later, after this release is merged:

```sh
claude plugin install jobscout --marketplace mlohmann/ai-skills
```

Inside Claude Code, the equivalent is `/plugin install jobscout --marketplace mlohmann/ai-skills`. This registers the repository marketplace and installs JobScout. Ask to configure JobScout in a new chat. If an older client lacks this option, use the local skill installer below or update the client. Avoid installing both the plugin and a duplicate personal skill.

### Local skill installer: Claude Code or Codex

Fetch `https://github.com/mlohmann/ai-skills` into a fresh temporary directory, inspect `agents/scripts/install.py` and `agents/scripts/package.py`, then run one of the following from the cloned repository:

```sh
python3 agents/scripts/install.py --host claude-code
python3 agents/scripts/install.py --host codex
```

Run only the command for the current host. Python 3.9+ is required. Claude Code installs under `~/.claude/skills/job-search-jev`; Codex under `~/.agents/skills/job-search-jev`. The installer never replaces an existing skill or writes a profile. If an installation exists, explain that an update needs review and preserve it. Start a new chat to discover the installed skill, then say “Configure JobScout.” The installer's `--skills-dir PATH` supports a user-selected project skill directory.

Do not run shell commands in a host without terminal support, write to shared locations without authorization, or claim installation succeeded without checking the destination's `SKILL.md`.

### Claude.ai

Use the uploadable [Claude skill ZIP](https://github.com/mlohmann/ai-skills/raw/refs/heads/main/agents/releases/0.2.0/job-search-jev-claude.zip). Enable code execution/file creation if required by the account, then use Customize > Skills > + > Create skill > Upload a skill. Menu names and availability can vary by account. If you can operate this surface with the user's authorization, complete the upload; otherwise give the user this download and the exact remaining steps. Never call an instruction paste an installed skill. Once enabled, ask Claude to configure JobScout. See `claude/setup.md` for the private Project fallback.

### ChatGPT

If the account supports local/repository skill plugins, use [the plugin package](https://github.com/mlohmann/ai-skills/raw/refs/heads/main/agents/releases/0.2.0/jobscout-chatgpt-plugin.zip) or the repository catalog `.agents/plugins/marketplace.json`. The root catalog points JobScout at `./agents`. This skill-only plugin has no MCP server or authentication requirement; JEV is a separate optional connection. Follow the host's supported installation flow and disclose any step requiring user interaction. This package is not a public-directory listing until separately submitted and accepted.

Portable fallback: create a private ChatGPT Project, paste `chatgpt/instructions.md` into Project instructions, and attach `chatgpt/jobscout-guide.md` from the source kit. This single guide includes the workflow, onboarding form and starter sources; no plugin import or Python is required. Web search availability controls live discovery. The installing agent can prepare these files, but must say if the user still needs to create the Project or upload them. Ask “Configure JobScout” after adding them. See `chatgpt/setup.md`.

## Finish onboarding

Let the user answer conversationally or use `skills/job-search-jev/assets/profile-form.md`. Export the private profile separately from public skill files. Offer starter sources, an empty source board, or their own URLs; copy the selected `sources` array into their profile. Offer a private Markdown/CSV listings board. Assistant review is the default; connect JEV only after the user opts in and authenticates independently.

Before calling setup complete, confirm the skill/instructions can be read, the user has a private profile, and the selected source board and evaluator are clear. If live browsing is unavailable, explain that supplied listings can still be screened. Installation does not itself establish live source coverage or JEV connectivity.
