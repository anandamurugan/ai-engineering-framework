---
id: STD-CODE-001
title: Coding Standard
version: 0.4.0
status: Draft
category: Coding
owner: Framework PMO
review_cycle: P12M
mandatory: true
ai_consumable: true
human_review_required: true
effective_date: null
last_reviewed: null
supersedes: []
related_standards:
  - STD-ARCH-001
  - STD-TEST-001
  - STD-PR-001
  - STD-DEP-001
related_playbooks: []
tags:
  - coding
  - quality
---

# STD-CODE-001 – Coding Standard

## Purpose

Make code readable, secure, maintainable, testable, and safe for human ownership.
## Scope

Applies to human-, generated-, and AI-authored source, configuration, scripts, and migrations, independent of language.
## Definitions

- **Generated code:** Output produced mechanically from an authoritative source.
- **Dead code:** Unreachable or unused code without an approved compatibility purpose.
## Principles

Optimize for clarity, least surprise, explicit failure, minimal duplication, secure defaults, and maintainable change.
## Applicability

All production-bound code MUST follow this standard and any stricter approved technology profile.
## Mandatory Rules

1. **Readability.** Code MUST express intent through consistent naming, small cohesive units, and complexity proportionate to the problem. Evidence: review and static-analysis results.
2. **Modularity.** Responsibilities MUST be separated behind explicit interfaces and MUST follow approved dependency direction. Evidence: changed-module and dependency review.
3. **Errors.** Failures MUST be detected, classified, propagated or handled deliberately, and MUST NOT be silently discarded. Evidence: error-path tests.
4. **Logging.** Logs MUST be structured where supported, actionable, appropriately leveled, correlated, and free of secrets and unnecessary sensitive data. Evidence: logging review and tests.
5. **Configuration and secrets.** Environment-specific values MUST be externalized and validated; secrets MUST NOT appear in source, generated output, logs, examples, or default configuration. Evidence: configuration and secret-scan results.
6. **Input and secure coding.** Untrusted input MUST be validated at trust boundaries; authorization, encoding, cryptography, and output handling MUST follow approved security controls. Evidence: threat-linked tests and security review.
7. **Resources and concurrency.** Code MUST bound, release, and safely coordinate files, connections, memory, threads, tasks, locks, and other finite resources. Evidence: resource and concurrency tests where applicable.
8. **Duplication and comments.** Material duplicated logic MUST be removed or justified; comments MUST explain decisions or constraints and MUST match behavior. Evidence: reviewer assessment.
9. **Quality automation.** Changed code MUST pass the approved formatter, compiler or interpreter checks, static analysis, and relevant tests. Evidence: reproducible check results.
10. **Generated and AI code.** Generated code MUST identify its source and regeneration method; AI-generated changes MUST receive the same human review, tests, security checks, and ownership as human code. Evidence: disclosure and review record.
11. **Lifecycle.** Dead code MUST be removed; deprecated code MUST identify replacement, consumers, migration, and removal conditions. Evidence: usage analysis and deprecation record.
## Recommended Practices

- Teams SHOULD use domain language, immutable data where practical, early validation, and simple control flow.
- Teams SHOULD automate formatting and prefer composition over unnecessary inheritance or global state.
## Prohibited Practices or Anti-Patterns

- Code MUST NOT contain hard-coded credentials, unexplained suppression of checks, unbounded retry or resource use, swallowed errors, or copy-pasted security controls.
## AI Implementation Guidance

Agents MAY propose code only within approved scope. They MUST inspect local conventions, disclose generated changes, avoid adding dependencies without review, run available checks, and stop when requirements, security, concurrency, data, or behavior are uncertain.
## Human Review Guidance

Humans verify intent, correctness, maintainability, security, edge cases, generated-code provenance, and operational impact. AI agents cannot approve their own code.
## Required Evidence

- Changed files and rationale
- Formatter, analysis, build, test, security, and secret-scan results available to the team
- Generated-code source, AI disclosure, review findings, and unresolved risks
## Validation Rules

- Automated checks SHOULD enforce formatting, static analysis, secret detection, dependency policy, and tests.
- Human review MUST assess clarity, design, error paths, resource safety, duplication, and lifecycle.
## Exceptions

Follow the [Standards Review Process](../../docs/governance/STANDARD_REVIEW_PROCESS.md); record affected rules, risk, controls, approval, expiry, and remediation.
## Related Standards

- [STD-ARCH-001 — Architecture Standard](../architecture/STD-ARCH-001-architecture-standard.md)
- [STD-TEST-001 — Testing Standard](../testing/STD-TEST-001-testing-standard.md)
- [STD-PR-001 — Pull Request Standard](../pull-request/STD-PR-001-pull-request-standard.md)
- [STD-DEP-001 — Dependency Management Standard](../dependency-management/STD-DEP-001-dependency-management-standard.md)
## Related Playbooks

None. Future relationships remain planned.
## References

- [Security Model](../../docs/architecture/SECURITY_MODEL.md)
- [Documentation Style Guide](../../docs/contributing/DOCUMENTATION_STYLE_GUIDE.md)
## Revision History

| Version | Date | Change | Author | Approval |
| --- | --- | --- | --- | --- |
| 0.4.0 | 2026-07-27 | Initial draft | Framework PMO | Pending Product Owner approval |
