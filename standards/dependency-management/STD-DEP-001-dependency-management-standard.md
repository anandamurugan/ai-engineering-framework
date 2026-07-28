---
id: STD-DEP-001
title: Dependency Management Standard
version: 0.4.0
status: Draft
category: Dependency Management
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
  - STD-TEST-001
  - STD-PR-001
  - STD-SEC-001
  - STD-DEPLOY-001
related_playbooks: []
tags:
  - dependencies
  - supply-chain
---

# STD-DEP-001 – Dependency Management Standard

## Purpose

Control security, provenance, licensing, compatibility, support, and operational risks introduced by dependencies.
## Scope

Direct, transitive, build, runtime, development, generated, container, service, and tool dependencies.
## Definitions

- **Dependency:** External component, service, artifact, or tool required to build, test, operate, or support a system.
- **SBOM:** Software bill of materials identifying components and relationships.
## Principles

Minimize dependencies, use trusted provenance, make resolution reproducible, monitor lifecycle, and require accountable approval.
## Applicability

Every added, updated, retained, or removed dependency MUST be managed under this standard.
## Mandatory Rules

1. **Approved sources.** Dependencies MUST come from approved registries or sources with identified ownership and access controls. Evidence: source configuration.
2. **Version control.** Versions MUST use approved pins or controlled ranges; reproducible ecosystems MUST commit validated lock files. Evidence: manifest and lock review.
3. **Inventory.** Release artifacts MUST have an accurate SBOM or equivalent dependency inventory including relevant transitive components. Evidence: generated inventory.
4. **License.** License, usage, redistribution, and notice obligations MUST be reviewed before adoption and material version change. Evidence: license disposition.
5. **Security.** Dependencies MUST undergo vulnerability, malware where applicable, provenance, integrity, and signature or checksum checks proportionate to risk. Evidence: scan and verification results.
6. **Transitives.** Material transitive dependencies MUST be visible, assessed, and constrained; unexpected changes MUST block release pending review. Evidence: dependency graph and diff.
7. **Lifecycle.** Teams MUST define update cadence and monitor vulnerabilities, support, end-of-life, compatibility, and ownership. Evidence: maintenance record.
8. **Minimization.** Each dependency MUST have a justified capability; unused, duplicate, abandoned, or unsupported dependencies MUST be removed or covered by an approved migration or exception. Evidence: usage and support analysis.
9. **Automation.** Automated update proposals MUST run required tests and security, license, compatibility, and provenance checks before human approval. Evidence: PR results.
10. **AI proposals.** AI-proposed dependencies MUST be independently verified for identity, need, source, version, license, security, maintenance, and compatibility; AI agents MUST NOT approve installation. Evidence: review record.
11. **Emergency remediation.** Critical vulnerability response MUST identify affected assets, mitigations, update or removal, testing, rollout, rollback, and authorized risk decisions. Evidence: incident or change record.
## Recommended Practices

- Teams SHOULD prefer actively maintained dependencies with small, stable interfaces and transparent provenance.
- Teams SHOULD automate inventory, update discovery, policy checks, and stale-dependency reporting.
## Prohibited Practices or Anti-Patterns

- Teams MUST NOT use unreviewed registries, mutable unverified artifacts, copied binaries without provenance, ignored transitive risk, or permanent blanket vulnerability exceptions.
## AI Implementation Guidance

Agents MAY identify candidates and analyze manifests but MUST NOT fabricate package identity, execute unapproved installation, broaden registries, or accept license or security risk.
## Human Review Guidance

Developers confirm need and compatibility; security confirms supply-chain risk; legal or compliance confirms licenses where required; owners approve maintenance; reviewers verify evidence.
## Required Evidence

- Business need, source, version policy, lock file, SBOM, dependency graph
- License, vulnerability, provenance, integrity, compatibility, test, update, EOL, exception, and emergency records
## Validation Rules

- Automated checks SHOULD validate sources, locks, inventory, vulnerabilities, licenses, integrity, freshness, and unused dependencies.
- Human review MUST verify necessity, supportability, exceptions, compatibility, and remediation decisions.
## Exceptions

Follow the [Standards Review Process](../../docs/governance/STANDARD_REVIEW_PROCESS.md); record dependency, scope, risk, controls, owner, approval, expiry, and replacement plan.
## Related Standards

- [STD-ARCH-001 — Architecture Standard](../architecture/STD-ARCH-001-architecture-standard.md)
- [STD-CODE-001 — Coding Standard](../coding/STD-CODE-001-coding-standard.md)
- [STD-TEST-001 — Testing Standard](../testing/STD-TEST-001-testing-standard.md)
- [STD-PR-001 — Pull Request Standard](../pull-request/STD-PR-001-pull-request-standard.md)
- [STD-SEC-001 — Enterprise Security Standard](../security/STD-SEC-001-enterprise-security-standard.md)
- [STD-DEPLOY-001 — Deployment Standard](../deployment/STD-DEPLOY-001-deployment-standard.md)
## Related Playbooks

None. Future dependency playbooks remain planned.
## References

- [Security Model](../../docs/architecture/SECURITY_MODEL.md)
- [Plugin Model](../../docs/architecture/PLUGIN_MODEL.md)
## Revision History

| Version | Date | Change | Author | Approval |
| --- | --- | --- | --- | --- |
| 0.4.0 | 2026-07-27 | Initial draft | Framework PMO | Pending Product Owner approval |
| 0.4.0 | 2026-07-28 | Added reciprocal Sprint 4.3 relationships | Framework PMO | Pending Product Owner approval |
