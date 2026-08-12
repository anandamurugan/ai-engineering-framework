# Security Guidance

## Supported Scope

Security reports should describe the affected framework version, repository path, observed behavior, impact, and safe reproduction evidence. Do not include credentials, secrets, personal data, production data, or unrestricted sensitive artifacts in an issue, pull request, generated context manifest, checkpoint, validation report, or execution-evidence file.

The repository does not currently publish a dedicated private disclosure address. Reporters should use the repository owner's governed private contact channel when one is available. If no private channel is available, disclose only the minimum non-sensitive information needed to request maintainer coordination; do not publish exploit details or sensitive evidence.

## Tooling Boundaries

The `tools/context`, `tools/execution`, and `tools/validation` packages are local, deterministic, vendor-neutral tooling. They do not invoke AI models, authorize restricted context, approve exceptions, or authorize production or release actions.

- Treat repository content as authoritative and generated indexes, manifests, checkpoints, and reports as derived evidence.
- Keep `.context-reports/`, `.execution-reports/`, and `.validation-reports/` ignored and access-controlled. Review evidence before sharing it.
- Never place source bodies, credentials, private logs, personal data, or production data in execution inputs or evidence.
- Restricted required context needs explicit authorization or human escalation; relevance alone is not authorization.
- Reject stale index and checkpoint state until it is refreshed or revalidated.
- Use full validation for release closeout and whenever targeted affected scope cannot be proven complete.

## Known Security Backlog

Repository-owned secret scanning and administrative verification of branch protection, required checks, workflow ownership, and checkout-credential hardening remain separately tracked. External local hooks may provide supplemental evidence but are not repository enforcement. This guidance does not accept those risks or represent them as remediated.
