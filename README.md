# AI skills, starting with JobScout

JobScout helps people review job opportunities against their own experience and search criteria. It combines reusable instructions for AI assistants with Python helpers that check required filters, prepare evaluation requests, and rank supplied listings.

The goal is to make a job search easier to inspect: show why a role qualifies, keep missing facts visible, and separate verified evidence from assistant judgment.

[Install JobScout](agents/INSTALL.md) · [How it works](#how-jobscout-works) · [Verification](#verification) · [Other skills](#other-skills)

## Try JobScout

For Claude Code clients that support the `--marketplace` option:

```sh
claude plugin install jobscout --marketplace mlohmann/ai-skills
```

Start a new chat and ask to configure JobScout. Keep your profile outside the repository. JEV is optional and stays off unless you explicitly authorize it.

Prefer another setup? See the [installation guide](agents/INSTALL.md) for the local skill installer, Claude.ai, and ChatGPT Projects. The [installation check record](agents/tests/installation-checks.md) states which routes have been tested.

## How JobScout works

1. Load your private search profile and application history.
2. Review supplied employer listings or retrieve evidence through permitted sources. Starter job-board entries are manual links.
3. Check salary, location, seniority, freshness, and application history before ranking fit.
4. Put missing or conflicting facts in a review queue. Keep assistant assessments separate from optional JEV results.
5. Save results to a private board. A scan does not submit applications or send messages.

### Example: required filters come first

These synthetic examples illustrate the ranking helper's behavior. They are not real vacancies or search results.

| Listing evidence | Fit score | Result |
| --- | --- | --- |
| Required filters pass and history is checked | 80 | Qualified when the minimum fit is 70 |
| Location eligibility is unknown | 80 | Review |
| Application history records an application | 80 | Excluded |

A fit score is a rubric-based assessment, not a hiring probability.

## Engineering decisions

- **Keep deterministic checks in code.** Python validates inputs, applies required filters, matches listing identities, and calculates weighted scores. The host supplies evidence and assessments.
- **Make uncertainty visible.** Missing history, conflicting copies, unsupported scores, and unknown eligibility keep results in review.
- **Separate authorization from configuration.** Host instructions require explicit JEV authorization for a scan or named automation. The offline helpers also block request generation when JEV is disabled.
- **Reuse only matching evaluations.** The optional POSIX cache matches the exact request and concrete model version. Current listing status and application history still need a fresh check.
- **Keep packages reproducible.** An explicit public-file list, fixed archive metadata, and checksum tests help keep releases consistent and private files out.

The helpers use the Python standard library. They do not browse job boards or call JEV. Host instructions are not a security sandbox; read the [privacy](agents/PRIVACY.md) and [security](agents/SECURITY.md) limits.

## Verification

From the repository root, run:

```sh
python3 -m unittest discover -s agents/tests -v
python3 agents/scripts/package.py
```

Tests cover filtering, application history, duplicate evidence, input validation, JEV opt-in, cache validation, installation, and reproducible packages. See the [installation check record](agents/tests/installation-checks.md) for observed results and the [host acceptance checklist](agents/tests/acceptance.md) for checks that remain separate from Python tests.

The repository includes source and release packages for ChatGPT-compatible hosts, Claude.ai, and Claude Code. Hosted conversations, live source retrieval, and authenticated JEV inference have not been verified by the installation checks.

## Other skills

- [Software Engineering Application Review](skills/software-engineering-application-review/SKILL.md): audit a résumé against a role before tailoring it.
- [Software Engineering Career Review](skills/software-engineering-career-review/SKILL.md): assess candidacy, evidence gaps, and preparation priorities.

Reusable skills live in `skills/`. JobScout lives in `agents/`. The `templates/`, `references/`, and `evals/` folders support new workflows.

JobScout uses the [MIT license](agents/LICENSE). That license applies to JobScout code and instructions; it does not grant rights to third-party services or job-board content.
