# JEV integration

JEV is optional. The package contains no endpoint, account connection, or credentials.

[Connection](#connection) · [Recorded request contract](#recorded-request-contract) · [Response handling](#response-handling)

## Connection

1. Confirm that the user enabled JEV in the private profile.
2. Find the JEV tools available to the host.
3. Inspect their current input and response schemas.
4. Connect the current user's account through the host connection interface.
5. List available models before evaluation.

Do not ask the user to put keys in instructions or profiles. A skill does not install or authenticate an MCP server. If a script environment restricts network use, use the host's connected tools.

## Recorded request contract

Composio discovery on October 10, 2026 recorded the names `JEV_LIST_MODELS` and `JEV_EVALUATE_STATE`. Treat this as a dated reference. Direct MCP names and current schemas can differ.

The recorded `EVALUATE_STATE` input requires `state` and a nonempty named `questions` map. The optional `model` defaults to `jev-latest`. State can be text, an object, or an array.

Supported question examples in that record include:

| Type | Recorded shape |
| --- | --- |
| Choice | `{"type":"choice","criteria":{"match":"Evidence establishes target-role match","mismatch":"Evidence establishes another role","unknown":"Insufficient evidence"},"instructions":"Judge job against profile"}` |
| Score | `{"type":"score","criteria":["No match","Weak match","Partial match","Strong match","Excellent match"],"instructions":"Judge only the named criterion using candidate evidence and job description"}` |
| Noul | `{"type":"noul","instructions":"Does the job description explicitly require management of direct reports?"}` |

Score criteria have 2–10 ordered levels in the recorded contract. They are not a 0–100 input scale.

The ranking-request helper creates a `role_match` Choice question and a Score question for each positive-weight profile criterion. These examples describe request shapes. They do not prove that an evaluation ran.

## Response handling

Save the exact request and actual response in private storage. Inspect the live response schema before you map fields or normalize scores. This release review did not run authenticated JEV inference.

Confirm score indexing and the returned legend. Preserve raw answers, model names, timestamps, and actual confidence. If score or confidence interpretation is unsupported, leave the value null and keep the job in review. Do not infer confidence from fit or treat option probability as confidence without documented equivalence.

Role Choice can guide review. A hard exclusion still requires source evidence. See [the workflow](workflow.md#evaluation) for fallback and call-budget rules.

Recorded integration source: [Composio JEV toolkit](https://composio.dev/toolkits/jev).

## Reduce repeated work

Use a concise candidate evidence summary with the qualifications and limits that
affect fit. Omit contact information and the full résumé. Keep the original
posting and excerpts in private storage. Combine independent questions that use
the same evidence into one request when no hard gate depends on the answers.
When extraction can settle a hard gate, check it before asking for fit scores.

For each eligible or review-stage listing, check the current user's private
evaluation cache before calling JEV. After resolving the active model alias,
use the concrete version in the request and run
`jobscout.py cache-key REQUEST.json`. Use the resulting key as the filename
stem under `jev-cache/` in the private profile directory. Use this directory
only when the host can keep it private. Store only validated, complete responses
from actual successful JEV calls. Record the response model and timestamp.
Before using a hit, check that the model matches and validate the answer names
and values against the current request. Treat unreadable, invalid or missing
entries as misses. If the active alias cannot be resolved, skip cache reuse.
Leave the user's model selection and routing policy in place.

Recheck employer status, exact filters and application history on each scan.
Apply current thresholds to cached answers. Report cache hits separately from
live calls and count only live calls in current JEV usage. Delete the cache when
the user removes the candidate information that it was derived from.

For comparisons, reuse a fixed set of employer evidence and manually reviewed
outcomes. Compare single listings with small groups of listings using the same
model and rubric. Record missing or mismatched answers, review dispositions,
latency and provider tokens. Keep confidence thresholds until labeled examples
support a change.

## Opt-in cache workflow

Explicit user authorization for the current scan or named automation is required
before request generation, a live call, or cache reuse. A saved enabled flag is
not authorization by itself. Use a per-run profile with `enabled: true` only after
that authorization. Keep `required: false` for assistant fallback. Label fallback
results as assistant review. Do not expand the pilot automatically.

The local helper `scripts/evaluation_cache.py` does not call JEV. Use:

```text
python3 scripts/evaluation_cache.py PROFILE.json JOB.json PRIVATE_DIRECTORY
python3 scripts/evaluation_cache.py PROFILE.json JOB.json PRIVATE_DIRECTORY ENTRY.json
```

The first command returns `hit` or `miss`. The second stores a validated entry.
Use a directory in private local storage, outside shared and synced folders.
The directory must belong to the current user and have mode 0700. Files use
mode 0600. These permissions do not provide encryption.

ENTRY must contain `request` (the exact generated request), `model`, `evaluated_at` (an ISO timestamp with timezone),
`raw_response` (the actual nonempty response object), and `evaluation`.
The normalized evaluation must contain `provider: "jev"`, a documented
`confidence` from 0 to 1, and `scores` from 0 to 100 for exactly the score
question names. The host must first validate the actual provider response,
including role_match and score indexing, against the live schema. The helper
checks the normalized contract; it cannot authenticate provider provenance or
establish that normalization is correct. Do not store incomplete, failed, or
unsupported responses. Never invent confidence to make an entry valid.

Use the returned entry's evaluation on the current job, then run `jobscout.py
rank` with current history. Do not copy cached job status or history. Recheck
employer status and hard gates on every scan. Changes to the exact generated
request or concrete model version cause a miss. An unresolved model alias
blocks cache use; it does not block an authorized live evaluation.

Record pilot metrics in private run storage: listings checked, JEV candidates,
cache hits, live calls, failures, assistant fallbacks, latency, and provider
reported input tokens, cached tokens, output tokens, and cost. Use null when a
measurement is unavailable. Reused evaluations are not new JEV usage. Do not
claim a savings percentage until comparable runs supply measurements. Report
results for user review before expansion. To roll back, keep JEV disabled and
stop use of the helper. Delete derived cache files when candidate data is removed;
local deletion does not delete provider copies.

Provider retention, training use, processing regions, subprocessors, and deletion
controls remain unverified. Do not present this pilot as regulatory certification.
