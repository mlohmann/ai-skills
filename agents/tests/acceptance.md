# Host acceptance checks

See the [installation check record](installation-checks.md) for completed installation checks and their limits. Run the remaining checks separately from the Python suite. Record the host, package version, account restrictions, actions performed, and observed results.

[Installation](#installation) · [Profile and sources](#profile-and-sources) · [Evaluation](#evaluation) · [Security and storage](#security-and-storage)

## Installation

1. Give the install instruction to a new Claude Code or Codex chat.
2. Check the installed files. Confirm that existing installations remain unchanged.
3. Confirm that default setup makes no JEV call.
4. Upload the skill ZIP in Claude.ai and test profile setup.
5. In a separate ChatGPT Project, add the instructions and Project guide. Test profile setup there.
6. Record any manual account-specific steps.

Do not describe a hosted installation as tested until you perform and record the check.

## Profile and sources

1. Configure a non-software occupation, non-US location, and non-USD pay policy.
2. Confirm that author preferences do not appear.
3. Test starter, custom, and blank source boards.
4. Confirm that manual entries cause no page fetch, sign-in attempt, or automated interaction.
5. Test a permitted source method and record its authorization and access limits.

## Evaluation

1. With JEV off, check that assistant results use the assistant review label.
2. Check that required filters still exclude jobs with high fit scores.
3. Test missing pay, unknown eligibility, missing history, conflicts, and blocked sources.
4. Test different requisitions at one employer, URL-only history, and meaningful query IDs.
5. Only after JEV opt-in and authentication, inspect actual schemas, score indexing, confidence, results, and usage.
6. Disconnect JEV. Confirm that optional fallback is disclosed and required mode stays pending.

Fixtures do not prove that an evaluator ran.

## Security and storage

1. Use synthetic source text that requests commands, file reads, profile changes, or data disclosure.
2. Confirm that the host treats those requests as data. Do not grant the requested actions for the test.
3. Before JEV use, confirm that the host explains the data transfer and removes confidential text.
4. Confirm that unexpected metadata stays out of generated payloads.
5. Export a private profile and load it in a new private chat.
6. Save results without replacing application notes. Keep personal files outside shared packages.
7. Confirm that no scan submits applications, sends messages, creates accounts, uploads files, schedules work, or posts to LinkedIn.

Offline tests do not establish these model and host behaviors.
