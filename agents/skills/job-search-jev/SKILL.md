---
name: job-search-jev
description: Find, filter, verify and rank job listings against a configurable job-seeker profile using JEV typed evaluations. Use for job discovery or supplied-listing screening, not application submission.
---

Use JobScout for any occupation; configure criteria from the current user's needs.
Read [the workflow](references/workflow.md) before a search. Read [JEV integration](references/jev.md) when evaluating and [data contract](references/data-contract.md) when running helpers.
Start with [the profile template](assets/profile.template.json). Keep credentials and personal data out of the shared skill. If the user already supplied preferences, use them instead of restarting onboarding.

For fetched listings and job-alert leads, use [JEV-assisted evidence extraction](references/extraction.md) and `scripts/evidence.py` before ranking. Use host tools for retrieval, JEV for bounded evidence selection/classification, and code for exact values and hard filters. That reference also defines end-to-end measurement boundaries.
