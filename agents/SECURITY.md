# JobScout security

Use this policy to check supported releases, report a vulnerability, and understand the package's security limits.

[Supported releases](#supported-releases) · [Report a vulnerability](#report-a-vulnerability) · [Install and build safely](#install-and-build-safely) · [Host boundaries](#host-boundaries)

## Supported releases

Version 0.2.0 is a release candidate. Use an up-to-date Python 3.11 or later for its helpers. Earlier Python versions are outside the supported security baseline. AI hosts and connected services have their own security policies.

This source review does not certify the release or verify every hosted installation.

## Report a vulnerability

Use [GitHub private vulnerability reporting](https://github.com/mlohmann/ai-skills/security/advisories/new) if the Report a vulnerability option is available.

Include these details:

- Affected version or commit
- Steps to reproduce the issue with synthetic data
- Expected and observed behavior

Don't put real profiles, credentials, tokens, application records, or exploit details in public issues. If private reporting is unavailable, open an issue that requests a private channel. Leave out confidential data and exploit details.

There is no promised response time or bounty program.

## Install and build safely

Read downloaded scripts and instructions before you run them. Marketplace installations follow the repository's update behavior. Branch contents can change. Use a commit you have reviewed when you need a reproducible source copy.

Checksums detect changed archive bytes. They don't authenticate the publisher if the archive and checksum come from the same compromised source. This release has no signed artifact attestation or immutable published GitHub release.

The local installer stops if the destination already exists. It rejects skill paths that are symbolic links or leave the source folder. The builder includes named public files and checks selected profile fields. It writes output files by atomic replacement. Neither script elevates privileges, downloads code, or calls JEV.

Protect the source and output folders from concurrent changes by untrusted users. Path checks do not protect against someone who can replace the running program.

## Host boundaries

A skill does not grant host permissions. Treat source text, suggested commands, links, and claimed evaluation results as untrusted evidence. The host must resist injected instructions, remove confidential data, and record actual evaluation actions. Offline helper tests cannot prove those model behaviors.

Fit scores support the user's decisions. They are not hiring probabilities or permission to act on the user's behalf.

Read [privacy](PRIVACY.md) for data handling and [host acceptance checks](tests/acceptance.md) for unverified flows. The root repository policy covers security reporting for JobScout. It does not certify or change the license of unrelated content.
