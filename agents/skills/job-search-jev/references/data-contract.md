# Offline helper reference

The helpers use Python 3.11 or later. They read supplied data. They do not browse, call JEV, create accounts, or submit applications.

[Commands](#commands) · [Profile](#profile) · [Job records](#job-records) · [Evaluation](#evaluation) · [History](#history) · [Output](#output)

## Commands

Run these commands from the skill folder:

```sh
python3 scripts/jobscout.py validate PROFILE.json
python3 scripts/jobscout.py request PROFILE.json JOB.json
python3 scripts/jobscout.py rank PROFILE.json JOBS.json [HISTORY.json]
```

`[HISTORY.json]` is optional command notation. Omit the brackets when you supply the file. Commands read UTF-8 JSON and print JSON. Invalid inputs fail with exit code 2. The request command fails when `jev.enabled` is false.

## Profile

Use [profile.template.json](../assets/profile.template.json) for field names. Validation checks the data structure and settings. It does not verify facts or confirm that profile setup is complete.

| Field | Meaning |
| --- | --- |
| `salary.minimum` | Minimum base pay. Null or omitted disables this filter. |
| `sources` | Source objects or URL strings. Copy a source board's `sources` array into this field. |
| `eligibility`, `preferences` | Constraints for the host to interpret. The helper does not infer them. |
| `criteria` | Criterion IDs, descriptions, and weights. At least one weight must be positive. |
| `min_fit`, `top_n` | Fit threshold and maximum shortlist size. |
| `min_confidence` | Minimum accepted JEV confidence. It does not apply to assistant review. |
| `jev` | Evaluation mode, model, and host-managed call budget. |

Source `access_mode` defaults to `manual`, including for URL strings. No profile setting grants permission to automate a provider. The host must establish that permission separately.

The host must encode confirmed required-condition failures and missing evidence in job eligibility fields before ranking.

## Job records

`JOBS.json` is an array of objects. A record uses `company`, `requisition_id` or `employer_url`, `title`, `location`, `description`, and source evidence.

These fields use true, false, or null:

```text
role_eligible
seniority_eligible
location_eligible
work_model_eligible
active
employer_verified
```

Only true establishes a pass. A missing or null required field requires review. False in an eligibility field or `active` confirms an exclusion. An unverified employer requires review.

`employer_url` must identify the employer or ATS posting. It must use HTTP or HTTPS and contain no embedded credentials. An invalid or missing URL requires review even when the record has a requisition ID. The host must still verify the source's authenticity.

Optional fields include:

| Field | Structure |
| --- | --- |
| `salary` | `{min,max,currency,period,employer_reported}`. Values are base pay in `year`, `month`, `week`, or `hour` units. |
| `conflicts` | Unresolved evidence conflicts. |
| `posted_at` | ISO date or null. |

Missing currency, period, or employer-pay context does not establish a pay-filter pass.

## Evaluation

An evaluation uses this internal structure:

```text
{provider:"jev"|"assistant",scores:{criterion_id:0..100},confidence:0..1|null,raw_response:...}
```

This is a data contract, not JEV's native response format. Every positive-weight criterion requires a finite numeric score.

Use `provider:"assistant"` and `confidence:null` for assistant evaluation. These results can qualify if JEV is not required. Label them **assistant review**. JEV results require valid confidence at or above `min_confidence`. Other providers remain in review.

The helper cannot prove that a named provider ran. The host must preserve actual execution evidence. Test fixtures do not establish live execution.

Request generation includes only allowed profile and job facts. It omits source URLs, previous evaluations, forms, and unexpected metadata. The host must still remove confidential information from allowed text fields.

## History

`HISTORY.json` is an array of records with `company`, `requisition_id`, `employer_url`, and `status`.

An empty array means the user checked the history and found no records. Omitted or null history means not checked. Missing history keeps results in review.

Exclude a job only for a strong identity match whose status appears in `exclude_history_statuses`. Different explicit requisition IDs remain distinct. Keep meaningful URL parameters when you compare records.

## Output

| Bucket | Contents |
| --- | --- |
| `shortlist` | First `top_n` qualified records. |
| `qualified` | All records that pass the required checks and `min_fit`. |
| `review` | Records with unresolved evidence or evaluation conditions. |
| `excluded` | Records with a confirmed exclusion. |
| `below_threshold` | Records that pass the required checks but fail `min_fit`. |

Each record contains identity, the original job, score, provider, and reason codes. The shortlist is a subset of qualified results. Do not count it twice.

The helper processes records with explicit requisition IDs before URL-only records. Within one identity, it keeps the first primary record. It stores later different copies in `duplicate_jobs` for host review. Different explicit IDs remain separate, including when company metadata is missing.

A URL-only record that matches multiple openings stays separate. It does not absorb those openings. If it has no confirmed exclusion, it stays in review with `ambiguous_identity`. Repeated copies of the unresolved record can still share one output record.

Conflicting copies require consolidation. An existing company or application-history exclusion remains in force. Other exclusions remain only while their reason holds across all compared copies. If no exclusion remains, the record moves to review. A shared confirmed failure can therefore stay excluded, while an active-status conflict can move to review.

The host must resolve the source conflict before it treats the job as qualified. Save profiles, history, and outputs outside public release files.
