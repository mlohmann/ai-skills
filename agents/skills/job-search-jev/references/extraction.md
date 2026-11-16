# Evidence extraction

Use the AI host to retrieve permitted source content. Use the helper to collect candidate evidence from that content.

[Collect](#collect) · [Review without JEV](#review-without-jev) · [Optional JEV request](#optional-jev-request) · [Resolve](#resolve) · [Measurement](#measurement)

## Collect

Run this command from the skill folder:

```sh
python3 scripts/evidence.py collect SOURCE.json
```

The input contains `text`, an optional `url`, and known source metadata. Verify alert leads against employer postings. Do not send personal forms, full résumés, or private inbox content to an external service.

When you read job alerts, return only the metadata and job links needed for review. Keep raw email MIME and account-security links out of evaluator requests.

The collector removes basic HTML and content after an “Apply for this job” heading. It returns pay candidates with exact excerpts and text offsets. The SHA-256 hash identifies the resulting listing text. Location lines are hints, not eligibility decisions.

The number parser supports common English currency formats. It does not support every language or pay format. Inspect the original source for these cases:

- A bare dollar sign with no established currency
- Ambiguous decimal grouping or mixed `k` and plain endpoints, such as `90–120k`
- Missing candidates, reversed ranges, or more than eight candidates
- Unclear currency, pay period, pay type, or geographic scope

Do not establish eligibility from collector output alone.

## Review without JEV

The host reviews evidence directly by default. Select supported facts, record short excerpts, and keep uncertainty visible. Apply the active profile's required filters. No JEV request is needed.

## Optional JEV request

Only when JEV is enabled, run:

```sh
python3 scripts/evidence.py request EVIDENCE.json PROFILE.json
```

The helper creates Choice questions for an existing pay-candidate ID, role, seniority, and location. It sends at most eight candidates in the generated context. It omits source metadata. JEV does not browse or return arbitrary extracted JSON.

Inspect the actual connected tool schema before you execute the request. Apply [the privacy rules](privacy.md) to all allowed text.

## Resolve

Convert the actual response into this internal format:

```text
{answers:{question:{choice,confidence}}}
```

This format is not a statement about JEV's native response fields. Keep the original request, response, and source evidence in private storage.

Run this command with the active profile's confidence threshold:

```sh
python3 scripts/evidence.py resolve EVIDENCE.json RESPONSE_DATA.json --confidence-floor 0.85
```

The example uses `0.85`. Replace it if the active `min_confidence` differs. Python callers can use `resolve(e,response,confidence_floor=...)`.

Invalid choices, missing confidence, and unknown answers require review. A selected pay candidate does not establish applicable base pay. The host must check currency, period, location, and pay type against the original source.

Direct contradictory evidence takes precedence over model classification. Do not spend ranking calls on confirmed exclusions. The host tracks the shared extraction and ranking call budget.

## Measurement

For a measured run, record these values:

- Start and end timestamps, with phase durations. State whether they use wall time or a monotonic clock.
- Tool counts and failures
- Sources attempted, completed, partial, or blocked
- Message and listing counts, duplicate reasons, and exclusion reasons
- Actual JEV usage by phase
- Host token-counter changes, with cached input separate when available

Record setup and final reporting separately. Report costs only from returned billing data or verified rates. Otherwise, report cost as unknown.

Compare the same scope and time window. State differences in context, cache, and execution order. Tool-response bytes are not tokens. These measurements alone do not prove a causal saving.
