# Offline helper contract

Python 3.11+, standard library only. These helpers do not browse, call JEV, create accounts or submit applications.

```
python3 scripts/jobscout.py validate PROFILE.json
python3 scripts/jobscout.py request PROFILE.json JOB.json
python3 scripts/jobscout.py rank PROFILE.json JOBS.json [HISTORY.json]
```

Paths are relative to the skill folder. Commands read UTF-8 JSON and print JSON; invalid inputs fail with exit code 2. `request` is disabled when `jev.enabled` is false. `validate` checks shape and settings, not factual truth or onboarding completeness. A null or omitted `salary.minimum` disables the pay floor.

The profile template is the source of field names. Sources may be URL strings or the source objects in `sources.starter.json`. To select a source board, copy its `sources` array to the profile. `eligibility` and `preferences` preserve user constraints for host interpretation; helpers cannot infer them. The host must encode all confirmed must-have failures and unresolved constraints in eligibility gates before ranking.

JOBS is an array of objects with `company`, `requisition_id` or `employer_url`, `title`, `location`, `description` and source excerpts/URLs. The gates `role_eligible`, `seniority_eligible`, `location_eligible`, `work_model_eligible`, `active`, `employer_verified` are true/false/null. Only true establishes a pass. `employer_url` is the canonical employer/ATS posting. Optional `salary` has `{min,max,currency,period,employer_reported}`; values are base pay in the declared period (`year`, `month`, `week`, `hour`). Missing context is not a salary pass. `conflicts` lists unresolved conflicts; `posted_at` is an ISO date or null.

Optional `evaluation` has `{provider:"jev"|"assistant",scores:{criterion_id:0..100},confidence:0..1|null,raw_response:...}`. All positive-weight criteria need finite numeric scores. Assistant evaluations use `confidence:null` and remain explicitly labeled assistant review. They can qualify when JEV is not required; the JEV confidence threshold applies only to JEV evaluations. Providers other than these stay review. Offline code cannot attest that the claimed provider really ran: the host must preserve real execution provenance. Fixtures never establish live execution.

HISTORY is an array of `{company,requisition_id,employer_url,status}`. An empty array means checked and empty; omitted/null means not checked and keeps results in review. Exclude only strong matching identities with statuses in `exclude_history_statuses`. Different explicit requisition IDs at the same employer remain distinct. Meaningful URL query parameters are preserved.

Output buckets: `shortlist` (first `top_n` qualified entries), `qualified` (all), `review`, `excluded`, `below_threshold`. Each record has identity, original job, score, provider and reason codes. Shortlist is a subset of qualified, not a second count of jobs. Conflicting duplicate records retain the first version and require host consolidation; they are not evidence of automatic reconciliation. Private profiles and outputs belong outside public release files. `employer_url` must be a valid HTTP(S) URL without embedded credentials even when a requisition ID exists; invalid/missing links stay review. Request generation projects allowed candidate/job facts, omitting source URLs, prior evaluations, forms and unexpected metadata; allowed text fields still require host redaction. Imported provider/verified flags are never execution provenance. Source `access_mode` defaults to `manual`; this helper does not retrieve sources or grant automation permission.
