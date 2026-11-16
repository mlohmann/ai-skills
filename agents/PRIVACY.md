# JobScout privacy

JobScout is distributed as instructions and local Python helpers. The helpers do not make network requests, collect telemetry, or send files to the author. They generate JSON payloads, and the host agent controls whether and where to send them. This does not establish that the AI host or optional connected services process data locally.

| Data | Processing and storage |
| --- | --- |
| Conversation, uploaded profile or résumé | Processed by the selected AI host under its account settings and terms. A résumé is optional. |
| Private profile, board, history or evidence saved locally | Ordinary files at the user's chosen private destination. No built-in encryption, deletion schedule or shared-folder protection. |
| JEV evaluation context | Off by default. If enabled, the host can send minimal candidate facts/preferences, eligibility, rubric and job evidence to the user's connected evaluation service. Helpers omit unexpected metadata, URLs, forms and previous evaluations; allowed free text still needs review/redaction. |
| Source requests | Made only by available host tools through provider-permitted methods. All starter sources default to manual discovery. Requests may reveal search terms and network/account metadata to the relevant provider. |
| Public packages | Generic templates and named source files only. Populated personal profile templates fail the build. No user profiles, run history or credentials are intentionally included. |

Use a private workspace outside the source/installed skill. Do not put personal materials in publicly shared Project knowledge. Do not supply secrets, identity documents, protected-trait data or third-party confidential information. Delete local data when no longer needed; separately use each host/provider's controls for their stored copies. This project does not provide a hosted deletion or data-subject request endpoint because it operates no hosted profile database.

Read [the host privacy workflow](skills/job-search-jev/references/privacy.md) before using external tools. There is no blanket GDPR, CCPA, SOC 2 or security-certification claim. The actual host/connector contracts, processing regions and retention terms are outside the code review. JobScout and JEV/ChatGPT/Claude/job boards are separate products; no endorsement is claimed.
