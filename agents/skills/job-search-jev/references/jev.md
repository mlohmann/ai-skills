# JEV integration

Verified tool-input contract via Composio discovery on 2026-10-10. There was no Active JEV connection and no live inference was executed. This package carries no endpoint, account or credentials.

Discover the host's JEV tools; Composio names are JEV_LIST_MODELS and JEV_EVALUATE_STATE. Inspect live schemas because direct MCP names may differ. Authenticate the current user's account through the host connection UI; never ask them to paste keys into instructions. List available models before evaluating. A skill doesn't itself install or authenticate an MCP server. Claude skills execute scripts in a sandbox; use connected tools for external evaluation when network access is restricted.

EVALUATE_STATE requires `state` and a nonempty named `questions` map; optional `model` defaults to `jev-latest`. State may be text, object or array. Question types:
- Choice: `{"type":"choice","criteria":{"match":"Evidence establishes target-role match","mismatch":"Evidence establishes another role","unknown":"Insufficient evidence"},"instructions":"Judge job against profile"}`.
- Score: `{"type":"score","criteria":["No match","Weak match","Partial match","Strong match","Excellent match"],"instructions":"Judge only the named criterion using candidate evidence and job description"}`. Ordered 2–10 levels; not a 0–100 input scale.
- Noul: `{"type":"noul","instructions":"Does the job description explicitly require management of direct reports?"}`.

The helper generates role_match Choice plus one Score per profile criterion. Save the exact request and actual response privately for audit. Read the real response schema before mapping its fields; output envelopes, score indexing and confidence scale have not been live-tested here. Store normalized scores/confidence only when supported, otherwise null and review. Do not infer confidence from fit. Role Choice supports review routing, but hard exclusion still requires source evidence.

Source: https://composio.dev/toolkits/jev
