# Claude setup

Claude.ai: upload `dist/job-search-jev-claude.zip` through your account's custom Skills interface when available. Enable the skill, connect a JEV MCP integration using your own account, and say “Configure JobScout for my job search.” If Skills are unavailable, create a private Project and use `project-instructions.md` plus the generic template/references. Network and tool access vary; the skill never supplies credentials.

Claude Code: copy `skills/job-search-jev/` into `.claude/skills/job-search-jev/` in a chosen project or `~/.claude/skills/job-search-jev/` for your own installation. Configure a JEV MCP server separately using your provider's actual setup. This build does not install it or create a server.

Claude API / Managed Agents: the skill ZIP can be uploaded through the supported skill API, then attached to an agent. External JEV calls need tools in the host orchestration layer; skill sandbox network access is not assumed.

Official reference: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
