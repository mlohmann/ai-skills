# Install JobScout

Use the section for your AI host. The release must be merged into the default branch before the public installation links work.

[Start in chat](#start-in-chat) · [Claude Code](#claude-code) · [Local skill installer](#local-skill-installer) · [Claude.ai](#claudeai) · [ChatGPT](#chatgpt) · [Agent checks](#agent-checks) · [Profile setup](#profile-setup)

## Start in chat

Give your agent this instruction:

> Read https://raw.githubusercontent.com/mlohmann/ai-skills/main/agents/INSTALL.md and install JobScout for this environment. Help me create my private profile and choose a starter source board or my own sources. Leave JEV off unless I opt in.

Your agent can guide setup. It can't grant new tools, bypass workspace policies, or complete steps that require your account access without authorization.

## Claude Code

For Claude Code 2.1.275 or later, run:

```sh
claude plugin install jobscout --marketplace mlohmann/ai-skills
```

Inside a Claude Code chat, use `/plugin install jobscout --marketplace mlohmann/ai-skills`. This command adds the repository marketplace and installs JobScout. In a new chat, ask Claude to configure JobScout.

If your client doesn't support this option, update it or use the local skill installer. Choose one installation method to avoid duplicate skills.

## Local skill installer

Use this method for Claude Code or Codex. It requires Python 3.11 or later.

1. Download [the repository](https://github.com/mlohmann/ai-skills) into a new temporary folder.
2. Read `agents/scripts/install.py` and `agents/scripts/package.py` before you run them.
3. From the repository root, run the command for your host.

For Claude Code, run:

```sh
python3 agents/scripts/install.py --host claude-code
```

For Codex, run:

```sh
python3 agents/scripts/install.py --host codex
```

If you extracted the source kit, run the same command without the `agents/` prefix from its `jobscout` folder.

The installer uses these locations:

| Host | Skill folder |
| --- | --- |
| Claude Code | `~/.claude/skills/job-search-jev` |
| Codex | `~/.agents/skills/job-search-jev` |

Use `--skills-dir PATH` to select another skill directory. The installer stops if JobScout already exists. It does not replace that installation or write a profile.

Start a new chat if the skill does not appear. Then ask your agent to configure JobScout.

## Claude.ai

1. Download [the Claude skill ZIP](https://github.com/mlohmann/ai-skills/raw/refs/heads/main/agents/releases/0.2.2/job-search-jev-claude.zip).
2. Enable code execution and file creation if your account requires it.
3. Open Customize > Skills. Click the + button, then choose Create skill > Upload a skill.
4. Upload the ZIP file and turn on the skill.
5. Ask Claude to configure JobScout.

Menu names and availability depend on your account. If Skills aren't available, use [the Claude Project setup](claude/setup.md).

## ChatGPT

### Plugin setup

If your host supports repository or local skill plugins, use [the ChatGPT plugin ZIP](https://github.com/mlohmann/ai-skills/raw/refs/heads/main/agents/releases/0.2.2/jobscout-chatgpt-plugin.zip) or the repository catalog at `.agents/plugins/marketplace.json`. The catalog points to `./agents`.

Follow your host's supported installation steps. There is no universal ChatGPT web ZIP-import step. This package includes no MCP server. JEV is a separate optional connection. A public directory listing requires its own submission and approval.

### Private Project setup

1. Create a private Project named JobScout.
2. Paste [the ChatGPT instructions](chatgpt/instructions.md) into Project instructions.
3. Attach `chatgpt/jobscout-guide.md` from the source kit.
4. Ask ChatGPT to configure JobScout and leave JEV off.

This setup uses instructions and a reference file. It does not require Python or a plugin installer. Use supplied employer listings if web search is unavailable. See [ChatGPT setup](chatgpt/setup.md) for details.

## Agent checks

Use these checks when you perform installation for a user:

1. Identify the host and its supported installation method.
2. Install only JobScout files. Do not install unrelated repository skills.
3. Preserve existing files and follow the user's workspace permissions.
4. Check the installed `SKILL.md` or Project instructions before you report success.
5. State which account-specific steps the user must still complete.
6. Read `skills/job-search-jev/SKILL.md` before profile setup.

Do not run shell commands if the host has no terminal. Do not report an instruction paste as a native skill installation. Do not connect JEV or another service without the user's instruction.

## Profile setup

Use [the profile form](skills/job-search-jev/assets/profile-form.md) or ask for missing information in chat. Keep the completed profile in the user's private destination. Do not copy the author's preferences.

Offer a starter source board, a blank board, or the user's own sources. Copy the selected board's `sources` array into the profile. Offer a Markdown or CSV results board. Confirm the profile before the first search.

All starter sources are manual links. Do not automate LinkedIn or Indeed pages or signed-in sessions. Use only a method that the provider permits. Before optional JEV use, explain the external data transfer and check allowed text for confidential information.

Before you finish, confirm that the user has a private profile and understands the selected sources and evaluator. Read [privacy](PRIVACY.md) and [security](SECURITY.md) for data handling and package limits. Installation alone does not verify live source retrieval or JEV connectivity.

### Optional application tracking

During setup, JobScout can offer read-only Gmail or Outlook access and a
Google Sheets or Excel tracker when your host supports the selected connection.
Choose the mail scope and workbook tab, then preview status changes before
enabling writes. You can also track applications manually.
See the [setup workflow](skills/job-search-jev/assets/profile-form.md#application-tracking).
