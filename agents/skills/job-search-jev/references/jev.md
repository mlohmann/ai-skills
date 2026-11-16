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
