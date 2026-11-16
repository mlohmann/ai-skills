# JobScout privacy

JobScout runs as instructions and local Python helpers. The helpers don't make network requests, collect telemetry, or send files to the author. Your AI host controls whether it sends generated requests to an external service.

[Where data goes](#where-data-goes) · [Keep your files private](#keep-your-files-private) · [Optional JEV](#optional-jev) · [Scope](#scope)

## Where data goes

| Data | Processing and storage |
| --- | --- |
| Chat content and uploaded profiles or résumés | Your AI host processes this content under its account settings and terms. A résumé is optional. |
| Saved profile, results board, history, or evidence | Files stay at the destination you choose. JobScout provides no built-in encryption or deletion schedule. |
| JEV evaluation context | JEV is off by default. If enabled, the host can send selected candidate facts, preferences, eligibility, rubric, and job evidence to your connected service. |
| Source requests | Host tools use methods permitted by the source provider. Requests might expose search terms or account and network metadata to that provider. All starter sources are manual links. |
| Public packages | The builder includes named source files and generic templates. It rejects selected personal fields in the profile template. This check does not detect all confidential text. |

Turning JEV off does not make ChatGPT or Claude processing local-only. Check the host's data settings before you upload files.

## Keep your files private

Choose a private folder outside the source repository and installed skill. Avoid public Project knowledge, shared Projects, and shared synced folders for personal material. Other members might be able to read those files.

Don't supply secrets, identity documents, protected-trait data, or another person's confidential information. Delete local files when you no longer need them. Manage host and provider copies separately through their data controls. Deleting a local file doesn't confirm deletion of service copies.

JobScout has no hosted profile database or hosted deletion endpoint.

## Optional JEV

Before enabling JEV, review the planned data transfer. The helpers omit unexpected metadata, source URLs, forms, and previous evaluations. Allowed text fields can still contain personal or confidential information. The host must remove that information before sending a request.

Check the connected service's retention terms, processing regions, and account controls. The code review did not audit those service contracts.

## Scope

Read [the host privacy procedure](skills/job-search-jev/references/privacy.md) before using external tools. The package makes no GDPR, CCPA, SOC 2, or security-certification claim.

JobScout, JEV, AI hosts, and job boards are separate products. No provider endorsement is claimed. The MIT license covers JobScout code and instructions. It does not license third-party content or services.
