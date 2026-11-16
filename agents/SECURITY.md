# JobScout security

## Supported releases

The 0.2.0 public-release candidate is the only JobScout version covered by this repository review. It is not yet a general-availability or certified release. Use an up-to-date Python 3.11 or newer for helpers; older Python versions are outside the supported security baseline. Host tools and optional services follow their own security policies.

## Report a vulnerability

Use [GitHub private vulnerability reporting](https://github.com/mlohmann/ai-skills/security/advisories/new) when “Report a vulnerability” is available. Include the affected commit/version, a minimal reproduction using synthetic data, and the expected/observed behavior. Do not put real profiles, credentials, tokens or private job/application records in public issues. If the private-report option is unavailable, open a sanitized issue requesting a private channel without exploit details or confidential data. No response-time commitment or bounty program is promised.

## Trust boundaries

Review scripts/instructions before executing a downloaded copy. Native marketplace installs follow the repository's update behavior; a mutable branch can change. Use an independently reviewed commit for reproducible evaluation. Archive checksums detect accidental changes but are not a publisher signature: a compromised source could change both a ZIP and its checksum. This release has no signed-artifact attestation or immutable published GitHub release yet.

The local installer refuses existing installations and escaping skill roots/files. The builder uses a public-file allowlist, populated-template checks and atomic output replacement. Neither script elevates privileges, downloads code or calls an evaluator. Protect the checkout/output directories from concurrent untrusted modification; path checks are not a sandbox against an attacker who can rewrite the running program.

The skill cannot expand host permissions. Source text, tool-like data, links, suggested commands and provider claims are untrusted. Host instructions require prompt-injection resistance, redaction and real provenance; offline helpers cannot prove those host behaviors. Scores are decision support, not calibrated hiring probabilities or authorization for actions.

See [privacy](PRIVACY.md) for data flows and `tests/acceptance.md` for remaining host verification. The root repository security policy covers reporting for JobScout; this license/policy does not relicense unrelated skills or third-party content.
