# ai-skills

Personal, portable AI skills and agent definitions.

This repository is intentionally small at the start: each skill should capture a proven, repeatable workflow rather than a generic prompt. Agent definitions compose those skills for a specific role or task.

## Structure

```text
skills/       Reusable capabilities; each skill lives in its own folder with SKILL.md
agents/       Role-specific instructions that can reference one or more skills
templates/    Starting points for new skills and agents
references/   Shared, durable context that more than one skill needs
evals/        Small, repeatable checks for skills or agents
```

## Start here

1. Copy `templates/skill/SKILL.md` into `skills/<skill-name>/SKILL.md`.
2. Replace every bracketed prompt with concise, task-specific guidance.
3. Add an agent only when a reusable role genuinely needs to compose multiple skills.
4. Add a focused evaluation case before relying on a skill for consequential work.

Keep credentials, private source material, and user-specific secrets out of the repository. Use local environment configuration for those values.
