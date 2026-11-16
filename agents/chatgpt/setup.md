# ChatGPT setup

Preferred reusable package: the repository root is a skill-only Agent Plugin (`plugin.json` plus `skills/`). Use your account's supported plugin import/marketplace workflow. Connect JEV independently via a compatible app/MCP integration. This is a package, not a published plugin or live service; it provides no MCP server itself.

Portable alternative: create a ChatGPT Project, paste `instructions.md` into project instructions, and attach the profile template, references and helper as needed. Keep your private profile in your private project/conversation, not in publicly shared knowledge. Start: “Configure JobScout for my job search.” Then “Find jobs using my profile and JEV.” Tools must be available to that project/account; a plain prompt doesn't grant connector access. Shared project access may expose project files: distribute the public package, and have recipients create their own private project.

For an eligible custom-GPT workspace, paste instructions into the builder, attach the generic reference/template files, enable web search and data analysis where available, and use connected apps for JEV. Check instruction length limits in the builder. New custom GPT creation is currently unavailable on personal accounts according to the linked help article. Do not invent an Actions endpoint; apps and actions cannot be combined in the same GPT. Publishing/import is account dependent and not performed by this repository build.

Official references (checked 2026-10-10):
- https://developers.openai.com/plugins/build/plugins
- https://developers.openai.com/plugins/build/skills
- https://help.openai.com/en/articles/8554397-creating-and-editing-gpts
