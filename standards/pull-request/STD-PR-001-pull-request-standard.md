---
id: STD-PR-001
title: Pull Request Standard
version: 0.4.0
status: Draft
category: Pull Request
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
  - STD-CODE-001
  - STD-API-001
  - STD-TEST-001
  - STD-DOC-001
  - STD-GIT-001
  - STD-DEP-001
related_playbooks: []
tags:
  - pull-request
  - review
---

# STD-PR-001 – Pull Request Standard

## Purpose

Provide focused, traceable, evidence-based, independently reviewed change control.
## Scope

Applies to changes proposed for protected branches, including code, configuration, documentation, dependencies, generated content, and emergency work.
## Definitions

- **Pull request (PR):** Review record proposing integration of a change.
- **Required owner:** Person or group accountable for an affected area, expressed through CODEOWNERS or equivalent.
## Principles

Keep changes small, make risk visible, automate repeatable checks, preserve separation of duties, and retain human accountability.
## Applicability

Changes to protected branches MUST use a PR or an approved equivalent with the same evidence and controls.
## Mandatory Rules

1. **Focused scope.** A PR MUST contain one coherent outcome, minimize unrelated changes, and state exclusions. Evidence: diff and description.
2. **Title and description.** The PR MUST summarize outcome, rationale, scope, work-item links, risks, and user or operational impact. Evidence: PR record.
3. **Evidence.** The PR MUST report tests executed and results, quality checks, security impact, architecture impact, dependency impact, documentation impact, deployment or migration needs, and rollback where applicable. Evidence: linked runs and artifacts.
4. **Ownership.** Required owners and domain reviewers MUST be assigned according to affected paths and risks; authors MUST NOT provide the sole required approval. Evidence: reviewer and approval record.
5. **Checks.** Required automated checks MUST complete successfully or have an authorized, recorded exception before merge. Evidence: immutable check results.
6. **Self-review.** The author MUST inspect the final diff, remove accidental content, resolve known issues, and confirm acceptance criteria before requesting review. Evidence: readiness statement.
7. **Findings.** Change requests MUST be resolved by change, evidence-based response, or authorized risk acceptance; unresolved blocking findings MUST prevent merge. Evidence: review thread disposition.
8. **Merge restrictions.** A PR MUST NOT merge while required approval, checks, conflict resolution, documentation, or evidence is incomplete. Evidence: branch-protection result.
9. **AI disclosure.** Material AI-generated or AI-modified content MUST be disclosed and receive accountable human review equal to human-authored work. AI agents MUST NOT approve or merge their own changes. Evidence: disclosure and approval.
10. **Emergency changes.** Emergency PRs MUST identify authority, incident or change record, minimized scope, validation, rollback, and retrospective review. Evidence: emergency record.
11. **Post-merge verification.** Changes with operational impact MUST define and record verification, monitoring, ownership, and response to failure. Evidence: observation or release record.
## Recommended Practices

- PRs SHOULD be small enough for one focused review and use draft status until evidence is ready.
- Reviewers SHOULD prioritize correctness, risk, maintainability, and evidence over style already enforced automatically.
## Prohibited Practices or Anti-Patterns

- Authors MUST NOT hide risk, split dependent changes to evade review, fabricate checks, dismiss findings without rationale, or use emergency labels for convenience.
## AI Implementation Guidance

Agents MAY prepare a branch, description, evidence summary, and responses. They MUST disclose uncertainty and AI contribution, preserve reviewer independence, and stop before approval or merge.
## Human Review Guidance

Humans confirm intent, evidence, risks, ownership, impacts, and finding resolution. Architecture, security, operations, and Product Owner gates apply according to scope and risk.
## Required Evidence

- Work item, final diff, acceptance mapping, test and check results
- Security, architecture, dependency, documentation, deployment, rollback, AI disclosure, approvals, and post-merge evidence as applicable
## Validation Rules

- Automated checks SHOULD enforce templates, ownership, approvals, branch status, tests, secrets, and policy gates.
- Human review MUST verify scope, evidence quality, impacts, findings, and accountable approvals.
## Exceptions

Follow the [Standards Review Process](../../docs/governance/STANDARD_REVIEW_PROCESS.md); emergency and routine exceptions require explicit human approval and expiry.
## Related Standards

- [STD-ARCH-001 — Architecture Standard](../architecture/STD-ARCH-001-architecture-standard.md)
- [STD-CODE-001 — Coding Standard](../coding/STD-CODE-001-coding-standard.md)
- [STD-API-001 — API Design Standard](../api/STD-API-001-api-design-standard.md)
- [STD-TEST-001 — Testing Standard](../testing/STD-TEST-001-testing-standard.md)
- [STD-DOC-001 — Documentation Standard](../documentation/STD-DOC-001-documentation-standard.md)
- [STD-GIT-001 — Git and Branching Standard](../git/STD-GIT-001-git-and-branching-standard.md)
- [STD-DEP-001 — Dependency Management Standard](../dependency-management/STD-DEP-001-dependency-management-standard.md)
## Related Playbooks

None. Future review playbooks remain planned.
## References

- [Pull Request Template](../../.github/pull_request_template.md)
- [Human-in-the-Loop Standard](../human-in-the-loop.md)
## Revision History

| Version | Date | Change | Author | Approval |
| --- | --- | --- | --- | --- |
| 0.4.0 | 2026-07-27 | Initial draft | Framework PMO | Pending Product Owner approval |
