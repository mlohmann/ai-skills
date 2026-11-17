# Set up JobScout in Claude

Choose the setup method for your account or app. JEV is off by default.

[Claude.ai](#claudeai) · [Claude Code](#claude-code) · [Private Project setup](#private-project-setup) · [Optional JEV](#optional-jev) · [References](#references)

## Claude.ai

1. Download `releases/0.2.1/job-search-jev-claude.zip` from [the release folder](https://github.com/mlohmann/ai-skills/tree/main/agents/releases/0.2.1).
2. Enable code execution and file creation if your account requires it.
3. Open Customize > Skills. Click the + button, then choose Create skill > Upload a skill.
4. Upload the ZIP file and turn on the skill.
5. Say “Configure JobScout.”

The ZIP contains one `job-search-jev/` folder with `SKILL.md` and its supporting files. Feature access and menu names can vary. Use a private Project if custom Skills aren't available.

## Claude Code

For Claude Code 2.1.275 or later, run this command after the release is merged:

```sh
claude plugin install jobscout --marketplace mlohmann/ai-skills
```

The repository catalog at `.claude-plugin/marketplace.json` points to `./agents`. In a new chat, ask Claude to configure JobScout.

To install a standalone skill instead, run this command from the cloned repository root:

```sh
python3 agents/scripts/install.py --host claude-code
```

The installer uses `~/.claude/skills/job-search-jev`. It stops if the skill already exists. Avoid installing both the plugin and the standalone skill.

For local plugin development, extract `jobscout-claude-code-plugin.zip` into a separate folder. Then run:

```sh
claude --plugin-dir /path/to/jobscout
```

This loads the folder for that session. Use the marketplace installation method for a persistent plugin installation. Keep `.claude-plugin/plugin.json` and `skills/` in their packaged locations.

## Private Project setup

1. Create a private Project.
2. Paste [project-instructions.md](project-instructions.md) into Project instructions.
3. Attach `chatgpt/jobscout-guide.md` from the source kit.
4. Ask Claude to configure JobScout.

This method uses shared reference material. It does not install a native skill. Search uses the tools available to your account.

## Optional JEV

To use JEV, connect your own provider through a supported integration. Check which tools are available before you evaluate a listing. The package supplies no server URL, credentials, or access to the author's accounts. Keep credentials out of skill files.

See [the installation guide](../INSTALL.md) for profile setup and source permissions.

### Optional application tracking

During setup, JobScout can offer read-only Gmail or Outlook access and a
Google Sheets or Excel tracker when your host supports the selected connection.
Choose the mail scope and workbook tab, then preview status changes before
enabling writes. You can also track applications manually.
See the [setup workflow](../skills/job-search-jev/assets/profile-form.md#application-tracking).

## References

These references were checked on November 15, 2026:

- [Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude)
- [Claude Code plugin manifest](https://code.claude.com/docs/en/plugins-reference)
