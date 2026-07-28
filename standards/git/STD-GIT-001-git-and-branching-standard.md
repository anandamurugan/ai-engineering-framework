---
id: STD-GIT-001
title: Git and Branching Standard
version: 0.4.0
status: Draft
category: Git
owner: Framework PMO
review_cycle: P12M
mandatory: true
ai_consumable: true
human_review_required: true
effective_date: null
last_reviewed: null
supersedes: []
related_standards:
  - STD-PR-001
related_playbooks: []
tags:
  - git
  - source-control
---

# STD-GIT-001 – Git and Branching Standard

## Purpose

Protect source integrity and provide traceable, recoverable collaboration without prescribing one model for every organization.
## Scope

Git repositories, branches, commits, merges, automation identities, releases, hotfixes, and AI-agent changes.
## Definitions

- **Default branch:** Primary integration branch designated by the repository.
- **Protected branch:** Branch whose writes and merges are controlled by policy and checks.
## Principles

Use a protected, releasable default branch, short-lived work, reviewable history, least privilege, and recoverable changes.
## Applicability

All governed repositories MUST define controls satisfying this standard; approved alternatives MAY adapt workflow without weakening outcomes.
## Mandatory Rules

1. **Protection.** Default and release branches MUST block unauthorized direct pushes, history rewriting, deletion, and bypass of required reviews or checks. Evidence: repository settings.
2. **Branches.** Work branches MUST use documented naming, trace to a work item, remain narrowly scoped, and be deleted or archived after integration. Evidence: branch and PR record.
3. **Synchronization.** Branches MUST incorporate relevant default-branch changes and resolve conflicts with validation before merge. Evidence: ancestry and check results.
4. **Commits.** Commits MUST be attributable, coherent, reviewable, and use meaningful messages; signing MUST be used where enterprise policy requires it. Evidence: commit history and signature status.
5. **Merge strategy.** Repositories MUST document an approved merge strategy that preserves required traceability, review evidence, and rollback. Evidence: settings and contribution guidance.
6. **Sensitive content.** Secrets and unauthorized sensitive data MUST NOT be committed; exposure MUST trigger revocation and incident handling, not only deletion. Evidence: scans and incident record.
7. **Files.** Large binaries and generated files MUST be excluded, externally managed, or explicitly justified with ownership and lifecycle. Evidence: repository policy and review.
8. **Reverts.** Reverts MUST identify the reverted change, reason, impact, validation, and follow-up; shared history MUST NOT be rewritten to conceal released defects. Evidence: revert commit and work item.
9. **Release and hotfix branches.** Their use, lifetime, source, merge-back, protections, and support scope MUST be documented; emergency status MUST NOT bypass human authority. Evidence: release process.
10. **Automation and AI.** Automation and AI agents MUST use distinct least-privilege identities and dedicated branches, MUST NOT push directly to protected branches, approve their own changes, or rewrite shared history. Evidence: identity and branch audit.
## Recommended Practices

- Teams SHOULD use trunk-based development with short-lived branches unless product or regulatory constraints justify another model.
- Teams SHOULD keep the default branch releasable and automate branch protection.
## Prohibited Practices or Anti-Patterns

- Users MUST NOT share automation credentials, force-push protected history, commit secrets, maintain indefinite unowned branches, or use branch names containing sensitive information.
## AI Implementation Guidance

Agents MAY create and update an explicitly authorized branch. They MUST inspect status, preserve unrelated work, avoid destructive history operations, disclose changes, and request human review before merge.
## Human Review Guidance

Repository owners approve protection and merge strategy. Reviewers verify traceability, history, conflicts, credentials, signatures where required, and emergency rationale.
## Required Evidence

- Branch-protection and merge settings, naming guidance, work-item and PR links
- Commit attribution, checks, secret scans, exception, revert, release, and automation identity records
## Validation Rules

- Automated checks SHOULD enforce protected branches, naming, signatures when required, secret scanning, and merge gates.
- Human review MUST assess exceptional history, large files, hotfixes, and bypass requests.
## Exceptions

Follow the [Standards Review Process](../../docs/governance/STANDARD_REVIEW_PROCESS.md); exceptions require owner, scope, risk, controls, approval, expiry, and remediation.
## Related Standards

- [STD-PR-001 — Pull Request Standard](../pull-request/STD-PR-001-pull-request-standard.md)
## Related Playbooks

None. Future source-control playbooks remain planned.
## References

- [Release Model](../../docs/architecture/RELEASE_MODEL.md)
- [Contributing](../../CONTRIBUTING.md)
## Revision History

| Version | Date | Change | Author | Approval |
| --- | --- | --- | --- | --- |
| 0.4.0 | 2026-07-27 | Initial draft | Framework PMO | Pending Product Owner approval |
