---
id: STD-DOC-001
title: Documentation Standard
version: 0.4.0
status: Draft
category: Documentation
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
  - STD-API-001
  - STD-PR-001
  - STD-DEPLOY-001
  - STD-REL-001
  - STD-INC-001
related_playbooks: []
tags:
  - documentation
  - knowledge
---

# STD-DOC-001 – Documentation Standard

## Purpose

Keep engineering knowledge accurate, accessible, version-aligned, reviewable, and sufficient to operate and support systems.
## Scope

Repository, architecture, API, operational, security, compliance, support, release, and troubleshooting documentation.
## Definitions

- **Documentation-as-code:** Version-controlled documentation reviewed with the change it describes.
- **Runbook:** Actionable operational procedure with conditions, safeguards, validation, and escalation.
## Principles

Documentation is a product artifact with an audience, owner, lifecycle, evidence, and human review.
## Applicability

Every system and material change MUST document information required to build, use, review, operate, secure, and support it.
## Mandatory Rules

1. **Ownership and audience.** Documents MUST identify purpose, intended audience, accountable owner, and review trigger or cycle. Evidence: document metadata or ownership record.
2. **Version alignment.** Behavior-changing work MUST update affected documentation in the same reviewed change or record an approved follow-up. Evidence: pull-request impact assessment.
3. **README.** Maintained repositories MUST provide purpose, status, setup, validation, support, security reporting, and authoritative navigation appropriate to users. Evidence: current README review.
4. **Architecture and decisions.** Material boundaries, quality attributes, data flows, deployments, and decisions MUST be documented with approved architecture views and ADRs. Evidence: linked architecture records.
5. **API documentation.** APIs MUST publish version-aligned machine-readable contracts or equivalent, semantics, examples, errors, access requirements, limits, ownership, and deprecation. Evidence: contract validation.
6. **Operations and support.** Production services MUST have runbooks, monitoring context, recovery, rollback, escalation, dependencies, known failure modes, and troubleshooting guidance. Evidence: operational readiness review.
7. **Security and compliance.** Required threat, data, access, control, exception, and compliance records MUST be maintained in authorized locations without exposing secrets. Evidence: specialist review.
8. **Release information.** Releases MUST document changes, compatibility, migrations, deprecations, known issues, security information, and recovery. Evidence: release notes.
9. **Links, diagrams, and examples.** Links MUST resolve; diagrams MUST have explanatory text; examples MUST be safe, current, and labeled non-normative where appropriate. Evidence: documentation checks.
10. **Operational knowledge.** Material knowledge MUST NOT exist only in individual memory, private messages, or unreviewed AI conversations. Evidence: authoritative runbook or decision record.
11. **AI content.** AI-generated documentation MUST receive accountable human review for accuracy, sources, sensitive data, unsupported claims, links, and current-state labels. Evidence: disclosure and approval.
## Recommended Practices

- Teams SHOULD keep documentation near its source and automate link, contract, and example checks.
- Documents SHOULD use plain language, accessible structure, and the [Documentation Style Guide](../../docs/contributing/DOCUMENTATION_STYLE_GUIDE.md).
## Prohibited Practices or Anti-Patterns

- Documentation MUST NOT contain secrets, fabricated results, stale instructions presented as current, inaccessible diagrams without explanation, or copied policy that creates conflicting authority.
## AI Implementation Guidance

Agents MAY draft and check documentation but MUST cite authoritative behavior, distinguish planned from implemented capability, avoid sensitive data, and stop when facts or approval are unavailable.
## Human Review Guidance

Owners confirm accuracy; architects, security, API, operations, and support reviewers confirm domain content; documentation reviewers confirm clarity and accessibility.
## Required Evidence

- Ownership, review date or trigger, source links, documentation impact assessment
- Link and example checks, specialist review, release alignment, unresolved gaps
## Validation Rules

- Automated checks SHOULD validate links, metadata, heading structure, contracts, examples, and prohibited secrets where tooling exists.
- Human review MUST verify accuracy, completeness, audience fit, accessibility, and current-state claims.
## Exceptions

Follow the [Standards Review Process](../../docs/governance/STANDARD_REVIEW_PROCESS.md) with risk, controls, approval, expiry, and remediation.
## Related Standards

- [STD-ARCH-001 — Architecture Standard](../architecture/STD-ARCH-001-architecture-standard.md)
- [STD-API-001 — API Design Standard](../api/STD-API-001-api-design-standard.md)
- [STD-PR-001 — Pull Request Standard](../pull-request/STD-PR-001-pull-request-standard.md)
- [STD-DEPLOY-001 — Deployment Standard](../deployment/STD-DEPLOY-001-deployment-standard.md)
- [STD-REL-001 — Release Management Standard](../release/STD-REL-001-release-management-standard.md)
- [STD-INC-001 — Incident Management Standard](../incident/STD-INC-001-incident-management-standard.md)
## Related Playbooks

None. Future documentation playbooks remain planned.
## References

- [Documentation Style Guide](../../docs/contributing/DOCUMENTATION_STYLE_GUIDE.md)
- [Knowledge Model](../../docs/architecture/KNOWLEDGE_MODEL.md)
## Revision History

| Version | Date | Change | Author | Approval |
| --- | --- | --- | --- | --- |
| 0.4.0 | 2026-07-27 | Initial draft | Framework PMO | Pending Product Owner approval |
| 0.4.0 | 2026-07-28 | Added reciprocal Sprint 4.3 relationships | Framework PMO | Pending Product Owner approval |
