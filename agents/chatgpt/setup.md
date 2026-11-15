# ChatGPT setup

Start with the one-line agent instruction in [INSTALL.md](../INSTALL.md). There are two supported packaging paths; availability depends on the host/account.

## Skill plugin

`releases/0.2.0/jobscout-chatgpt-plugin.zip` contains a portable root `plugin.json` and `skills/`. Use the host's supported local/repository plugin flow. The repository-root catalog `.agents/plugins/marketplace.json` points to `./agents`; the catalog inside `agents/` supports registering that folder directly. No MCP server or JEV account is required. Public-directory distribution is a separate submission/review step, not something a ZIP build performs. Do not assume a universal ChatGPT web ZIP-import button.

## Private Project, without a plugin installer

1. Create a private Project named JobScout.
2. Paste `instructions.md` into Project instructions.
3. Attach `jobscout-guide.md` as a Project file. It is generated from the shared skill, workflow, profile form, source guide and templates, avoiding many separate uploads.
4. Say “Configure JobScout. Help me fill out my profile and choose job sources. Leave JEV off.”
5. Save the resulting profile in your private Project. Add application history only if you want it checked. If you already applied nowhere, explicitly confirm an empty history; otherwise “not checked” is accurate.

Search uses the account's available web tools; without them, provide listings to screen. The helper scripts are optional for conversational use. Keep publicly shared packages generic and have each recipient create their own private Project. A shared Project may expose files to its members.

JEV is optional and needs the recipient's own authorized connection/tool. A Project or plugin does not create one. Public ChatGPT custom-GPT creation is not the distribution path for this release; account restrictions and migration notices vary.

Official setup references, checked November 15, 2026:
- [Projects in ChatGPT](https://help.openai.com/en/articles/10169521-projects-in-chatgpt)
- [Plugin packaging](https://developers.openai.com/plugins/build/plugins)
- [Skills](https://developers.openai.com/plugins/build/skills)
