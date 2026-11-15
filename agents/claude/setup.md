# Claude setup

Start with the one-line agent instruction in [INSTALL.md](../INSTALL.md).

Claude.ai: download `releases/0.2.0/job-search-jev-claude.zip` and upload through Customize > Skills > + > Create skill > Upload a skill, where available. Enable code execution/file creation if required. The ZIP contains one `job-search-jev/` folder with `SKILL.md` and its supporting files. Turn the skill on, then say “Configure JobScout.” No JEV account is needed.

If custom Skills are unavailable, create a private Project, paste `project-instructions.md` into instructions, and attach `chatgpt/jobscout-guide.md` from the source kit. It works as shared reference material for either host. This is the instruction-based fallback, not an installed skill. Search depends on the account's tools.

Claude Code (2.1.275+): install with `claude plugin install jobscout --marketplace mlohmann/ai-skills` after the release is merged. This uses the repository-root `.claude-plugin/marketplace.json` entry pointing to `./agents`. Ask to configure JobScout in a new chat. As a standalone skill alternative, run `python3 agents/scripts/install.py --host claude-code` from the cloned repository. It installs only JobScout into `~/.claude/skills/job-search-jev` and refuses to replace existing files. Restart the chat if needed and ask to configure JobScout. For plugin development/testing, unzip `jobscout-claude-code-plugin.zip` to a dedicated folder and run `claude --plugin-dir /path/to/jobscout`; a normal persistent plugin install follows Claude Code's marketplace flow. The plugin manifest is `.claude-plugin/plugin.json`; `skills/` stays at the package root.

If you choose JEV, connect your own provider through the host's supported integration and verify available tools. This package supplies no server URL, credentials or access to the author's accounts. Never paste credentials into skill files.

Official references, checked November 15, 2026:
- [Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude)
- [Claude Code plugin manifest](https://code.claude.com/docs/en/plugins-reference)
