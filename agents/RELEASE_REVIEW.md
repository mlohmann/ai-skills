# JobScout 0.2.0 release review

Reviewed November 15, 2026. Scope: JobScout under `agents/`, its repository discovery entry, public packages and installation instructions. Unrelated skills and the owner's active scan preferences are outside this release.

## Findings fixed

- Extraction hardcoded frontend senior IC roles, Washington eligibility and US annual pay. Questions now use the current user's profile. Unsupported numerical formats remain unknown.
- Optional JEV routed every assistant result to review, preventing assistant-only shortlists. Assistant results can now qualify under the same evidence gates, with explicit provider labels and no invented confidence. JEV defaults off; disabled request generation fails clearly.
- URL cleanup discarded meaningful query fields, merging distinct jobs. Query identifiers are retained; known tracking fields are removed. URL-only history can match ID-bearing jobs, while distinct explicit requisition IDs stay distinct.
- Salary collection included application-form pay questions because the cutoff happened after matching. The cutoff now precedes collection, and hashes/offsets use the same extracted text.
- Confidence accepted booleans, non-finite values and out-of-range values. Invalid or unseen choices were insufficiently flagged. These require review. The active confidence threshold can be passed explicitly.
- Malformed profiles, source URLs and evaluator shapes could crash or slip into scoring. Validation and readable CLI failures cover the changed boundaries.
- Recursive packaging risked including private runtime files. Packages and the installer use explicit public-file lists, reject escaping paths/symlinks, and produce deterministic archives with SHA-256 checksums. Existing installs are never replaced automatically.
- Host setup blurred native installs and instruction-based use. A consolidated Project guide and separate platform package layouts make the remaining account-specific steps explicit.
- The repository needed discovery and redistribution support. Its root OpenAI and Claude marketplace catalogs point to `./agents`; JobScout under `agents/` is MIT licensed. No authentication requirement is declared for the JEV-free skill.

## Verification

Run `python3 -m unittest discover -s tests -v` and `python3 scripts/package.py` from `agents/`. Regression cases cover evaluator modes, hard gates, history identity, query URLs, dates, exact pay extraction, profile validation, installation conflicts, archive layouts, checksums, reproducibility and exclusion of injected private files. Executed results are recorded in the accompanying release-preparation chat; this document does not substitute for execution.

## Remaining limits

No authenticated JEV calls, hosted ChatGPT/Claude.ai installs or live job searches were performed for this release review. The Python installer and native Claude Code one-command marketplace install were tested in isolated temporary configurations. Claude Code listed JobScout 0.2.0 enabled with one skill and no MCP servers or hooks. This verifies local registration and component discovery, not hosted-app use or a live model search. Host setup and starter sites were checked against official pages; permissions and tools vary. See `tests/acceptance.md` for live-host checks. The evidence collector is a bounded regex helper, not a universal salary parser or crawler. The host must supply factual gates and actual evaluator provenance; offline code cannot prove them.

Install/download URLs target the default branch and become public after merge. Building ZIPs does not publish them to either platform's directory. No applications, outreach, LinkedIn posts or public-directory submissions are part of this review.
