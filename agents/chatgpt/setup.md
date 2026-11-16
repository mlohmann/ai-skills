# Set up JobScout in ChatGPT

Choose a plugin installation if your host supports it. You can also use a private Project with instructions and one reference file.

[Plugin setup](#plugin-setup) · [Private Project setup](#private-project-setup) · [Search and JEV](#search-and-jev) · [References](#references)

## Plugin setup

Use `releases/0.2.0/jobscout-chatgpt-plugin.zip` with your host's supported plugin installation steps. The ZIP contains a root `plugin.json` and the `skills/` folder.

The repository catalog at `.agents/plugins/marketplace.json` points to `./agents`. The catalog inside `agents/` lets you register that folder directly. This plugin requires no MCP server or JEV account.

A ZIP build does not create a public directory listing. Submission and approval are separate steps. See [the installation guide](../INSTALL.md).

## Private Project setup

1. Create a private Project named JobScout.
2. Paste [instructions.md](instructions.md) into Project instructions.
3. Attach [jobscout-guide.md](jobscout-guide.md) as a Project file.
4. Say “Configure JobScout. Help me fill out my profile and choose job sources. Leave JEV off.”
5. Save your completed profile in the private Project.

The guide contains the workflow, profile form, source instructions, and templates. You don't need to upload each reference separately.

Add application history if you want JobScout to check it. Confirm an empty history only if you have checked that there are no records. Otherwise, use “history not checked.”

Share the generic package with others. Each person should create a private Project. Members of a shared Project might be able to read its files.

## Search and JEV

Search uses the tools available to your account. All starter sources are manual links. Automatic retrieval requires permission for the method used. Supply employer listings if browsing is unavailable.

The Python helpers are optional for chat use. JEV is also optional. It requires your own supported connection. A Project or plugin does not create that connection.

This release uses plugin and Project setup paths. It does not depend on creating a custom GPT. Feature access and account migration notices can vary.

## References

These setup references were checked on November 15, 2026:

- [Projects in ChatGPT](https://help.openai.com/en/articles/10169521-projects-in-chatgpt)
- [Plugin packaging](https://developers.openai.com/plugins/build/plugins)
- [Skills](https://developers.openai.com/plugins/build/skills)
