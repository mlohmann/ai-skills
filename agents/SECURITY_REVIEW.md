# JobScout security and release-compliance review

Reviewed November 15, 2026. This is a source, packaging and public-release readiness review of JobScout 0.2.0, not a penetration test or a legal/regulatory certification. The owner's personal checkout remains untouched; fixes are on the release PR branch.

## Findings and fixes

| Priority | Finding demonstrated on the previous release candidate | Resolution |
| --- | --- | --- |
| P1 | Ranking requests forwarded the complete job object to optional JEV; extraction forwarded source/header metadata. Synthetic private form/cookie fields appeared in outbound payloads. | Explicit field projection for candidate/job/extraction context, including nested metadata. Source URLs, forms, previous evaluations and unexpected fields stay out. Allowed text still requires host redaction. |
| P1 | Starter setup could direct an agent to automate Indeed/LinkedIn pages or a signed-in browser despite provider restrictions. No such access was performed by this review. | Starter entries explicitly manual; missing/legacy access mode also manual. Automated access requires permission for the specific method, not just login/user consent. Guides no longer suggest signed-in browsing as a workaround. |
| P2 | A symlink replacing the entire skill root passed installer checks and loaded files from outside the repo. | Reject symlinked/escaping skill roots before installation; check every allowlisted file before creating the install destination. |
| P2 | Writing an archive through a preexisting hard link changed the linked victim file in a synthetic reproduction. | Atomic temporary-file replacement for archives, consolidated guide and checksums. Existing symlinks are rejected. |
| P2 | A record with a valid requisition ID and a `javascript:` employer link could qualify when its supplied verification flag was true. No script execution occurred in the probe. | Independently require a credential-free HTTP(S) employer URL before qualification; invalid or missing URLs remain review. The host still must establish actual source authenticity. |
| P2 | Public template packaging could include a profile filled in place of the generic template; generic copy was clean at review time. | Add a build gate requiring blank personal fields, unconfigured pay/eligibility and JEV disabled, and reject unexpected top-level/template metadata. This is targeted protection, not universal secret detection. |
| P2 | Setup advertised Python 3.9+, including runtimes past security support. | Supported baseline is updated Python 3.11+; installer rejects older interpreters. |

## Privacy, license and permitted use

- No network client, subprocess-based downloader, analytics endpoint, credential store, dependency installer or author-operated profile database is present in shipped runtime Python code. JEV calls are performed by the host after opt-in, not these helpers.
- ChatGPT/Claude still process conversation/uploads. JEV off is not a claim of local AI processing. `PRIVACY.md` and the embedded privacy workflow describe minimization, redaction, retention/deletion boundaries and the user's responsibility for service settings.
- The package is job-seeker decision support with human career/application decisions. Instructions disallow employer-side candidate selection, protected-trait inference and unsolicited applications/messages/uploads. These are host workflow requirements, not cryptographic or sandbox enforcement.
- Public JobScout files and all four archives include the MIT license. Runtime Python uses the standard library only; no third-party Python dependencies are bundled. The MIT grant does not license external job content, brands or AI/connector services. Unrelated repository skills are outside the license/review scope. No independent copyright-chain investigation was performed.
- Provider terms were checked at the cited pages below. This review does not grant scraping rights or certify every user-selected source, connector or jurisdiction. Preserve short permitted excerpts and direct employer links; do not redistribute full protected listings or credentials.

## Verification and residual release work

Executed checks: 49 Python tests passed, including the reproduced data-transfer, filesystem and link failures plus populated-template rejection. Skill and Claude marketplace validators, focused Ruff checks and Git whitespace checks passed. Four rebuilt ZIPs matched their SHA-256 entries and contained license notices; 42 public text files and 86 archive members were scanned with targeted secret/private-path patterns and produced no matches. Runtime import inspection found only Python standard-library and in-package modules, with no network-client imports or dynamic-execution calls. These checks are bounded, not a universal secret or vulnerability scan. Test payloads use synthetic data.

GitHub private vulnerability reporting was checked and is currently disabled. Enable it before public promotion so the private report link in `SECURITY.md` works. This review did not change repository-wide settings; the sanitized public-issue fallback avoids disclosing exploit details while a private channel is arranged. No response SLA is promised.

Hosted ChatGPT/Claude.ai installs, live model prompt-injection resistance, JEV provider contracts/retention/regions and full real-host source-access compliance remain unverified. Current branch downloads and same-source SHA-256 files are not independent publisher authentication; a signed/immutable public release has not been created. Public-directory submission/approval and default-branch installation links remain dependent on merge and the respective platform process. No automated CVE scanner, independent penetration test, legal opinion or GDPR/SOC 2 certification was performed. This review found no critical issue in its inspected scope; it is not a guarantee that no vulnerability exists.

## Primary references checked

- [Indeed terms, September 29, 2026](https://www.indeed.com/legal?hl=en): restrict automated/agent access without the specified provider permission.
- [LinkedIn User Agreement, section 8.2](https://www.linkedin.com/legal/user-agreement): restrict scraping and unauthorized automated access, including third-party methods.
- [Python support status](https://devguide.python.org/versions/): Python 3.9/3.10 are end-of-life; 3.11 remains in security support.
- [MIT license](https://opensource.org/license/mit): preserve its copyright/permission notice with distributed code.
- [GitHub supply-chain security](https://docs.github.com/en/code-security/concepts/supply-chain-security/supply-chain-security): immutable releases and attestations address provenance; same-source checksums alone do not establish it.
