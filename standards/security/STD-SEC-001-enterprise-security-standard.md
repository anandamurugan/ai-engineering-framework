---
id: STD-SEC-001
title: Enterprise Security Standard
version: 0.4.0
status: Draft
category: Security
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
  - STD-DEP-001
  - STD-DEPLOY-001
  - STD-OBS-001
  - STD-REL-001
  - STD-INC-001
  - STD-RISK-001
related_playbooks: []
tags:
  - security
  - compliance
  - supply-chain
---

# STD-SEC-001 – Enterprise Security Standard

## Purpose

Protect identities, systems, software, data, and supply chains through risk-based controls that remain verifiable throughout engineering and operation.

## Scope

Applies to enterprise applications, APIs, data, infrastructure, delivery systems, dependencies, artifacts, human and machine identities, and AI-assisted engineering. Organization policy and law remain authoritative.

## Definitions

- **Machine identity:** Non-human identity used by a workload, service, automation, or agent.
- **Security exception:** Time-bound human authorization to deviate from a control with recorded risk and compensating controls.
- **Trust boundary:** Point where identity, privilege, data classification, or control changes.

## Principles

Security is designed in, continuously verified, least-privileged, defense-in-depth, Zero-Trust-aligned, separated by duty, data-minimizing, securely defaulted, and proportionate to risk.

## Applicability

Every production-bound system and material change MUST identify applicable security, privacy, identity, supply-chain, and compliance obligations. Stricter enterprise policy prevails.

## Mandatory Rules

1. **Security planning.** Teams MUST classify data and assets, identify trust boundaries and abuse cases, perform risk-based threat modeling, and assign control owners before material design approval. Evidence: threat model, data-flow record, and security plan.
2. **Identity and authentication.** Human, service, machine, and AI-agent identities MUST be unique, attributable, strongly authenticated according to risk, and prohibited from shared credentials. Evidence: identity inventory and authentication configuration review.
3. **Authorization and privilege.** Access MUST be explicitly authorized using role- or attribute-based controls, least privilege, separation of duties, and deny-by-default behavior; privileged access MUST be separately controlled and monitored. Evidence: access model and privileged-access record.
4. **Identity lifecycle.** Credential issuance, session duration, rotation, revocation, recovery, and periodic access review MUST be defined for every identity class. Evidence: lifecycle procedure and dated access review.
5. **Secrets.** Production secrets MUST use approved secrets-management mechanisms and MUST NOT appear in source, prompts, logs, generated documentation, deployment manifests, or unencrypted configuration. Evidence: secrets inventory and scan result.
6. **Cryptography.** Sensitive data MUST use approved encryption in transit and at rest; keys, certificates, algorithms, rotation, expiry, revocation, and custody MUST follow enterprise cryptographic governance. Evidence: cryptographic inventory and configuration review.
7. **Application controls.** Trust boundaries MUST enforce input validation, output encoding, injection prevention, authorization, secure errors, session protection, file-upload restrictions, data minimization, and abuse controls. Evidence: security design, tests, and code review.
8. **Security verification.** Applicable secure review, static analysis, dynamic analysis, composition analysis, secret scanning, artifact or container scanning, infrastructure-as-code scanning, security regression testing, and risk-based penetration testing MUST complete before release. Evidence: attributable results and finding disposition.
9. **Supply chain.** Builds MUST use approved sources, verified provenance, protected build identities, reproducible dependency resolution, software bills of materials, and integrity verification or signing where required by risk. Evidence: build record, SBOM, provenance, and verification result.
10. **Vulnerability management.** Vulnerabilities MUST have severity, affected scope, owner, remediation target, compensating controls, and human disposition; overdue critical findings MUST block release unless authorized risk acceptance exists. Evidence: vulnerability register and approval.
11. **Operational security.** Security-relevant activity MUST produce protected audit records and actionable monitoring; patching, escalation, incident handling, evidence retention, and control review MUST have accountable owners. Evidence: audit configuration, monitoring review, and response records.
12. **Metrics and compliance.** Owners MUST monitor scan coverage, critical-vulnerability age, mean time to remediate, exception count, secrets exposures, and control failures without suppressing valid findings to improve metrics. Evidence: dated metrics and corrective actions.
13. **Approval.** Security exceptions, control changes, unresolved high risk, sensitive-data use, and production access MUST receive authorized human approval; an AI agent MUST NOT approve or accept them. Evidence: approval record with scope, conditions, and expiry.

## Recommended Practices

- Teams SHOULD automate repeatable controls while retaining human review for context, risk, exceptions, and approval.
- Systems SHOULD minimize exposed interfaces, retained data, standing privilege, and trust in network location.
- Security exercises and control tests SHOULD include realistic abuse, recovery, and supply-chain scenarios.

## Prohibited Practices or Anti-Patterns

- Teams MUST NOT use hard-coded secrets, unsupported cryptography, shared privileged accounts, unverified artifacts, permanent blanket exceptions, or security-by-obscurity.
- Teams MUST NOT modify or omit evidence to create a false compliance result.

## AI Implementation Guidance

AI agents MAY draft threat models, controls, tests, findings, mitigations, and evidence summaries using authorized context. Agents MUST use minimum access, protect sensitive inputs, disclose uncertainty, preserve failed findings, and stop when identity, data, production, policy, or risk authority is unclear. Agents MUST NOT self-approve exceptions, change access, accept risk, suppress controls, or act as final security authority.

## Human Review Guidance

Security owners review threats, controls, findings, exceptions, and operational readiness. Identity, privacy, compliance, architecture, and operations reviewers participate where applicable. The accountable business owner accepts residual risk, and the Product Owner retains final approval of this standard.

## Required Evidence

- Threat model, security plan, data classification, identity and access review, and cryptographic inventory
- Security review record; SAST, DAST, composition, secret, artifact, and infrastructure scan results
- SBOM, provenance and integrity evidence, vulnerability disposition, and penetration-test result where required
- Operational monitoring, patch, incident, exception, approval, metrics, owner, retention, and review records

Evidence MUST be attributable, traceable to scope and version, retained under enterprise requirements, and reviewable without exposing secrets.

## Validation Rules

- Automated checks SHOULD validate metadata, prohibited secrets, dependency and artifact integrity, required scans, SBOM presence, and unresolved findings where tooling exists.
- Human review MUST assess threat coverage, identity and data controls, evidence quality, exceptions, residual risk, operational readiness, and required approvals.
- A tool result MAY demonstrate a control execution but MUST NOT be treated as security approval by itself.

## Exceptions

Exceptions follow the [Standards Review Process](../../docs/governance/STANDARD_REVIEW_PROCESS.md) and require affected rules, business justification, owner, risk, compensating controls, approver, effective and expiry dates, monitoring, and remediation. AI agents may draft but cannot approve an exception.

## Related Standards

- [STD-ARCH-001 — Architecture Standard](../architecture/STD-ARCH-001-architecture-standard.md)
- [STD-CODE-001 — Coding Standard](../coding/STD-CODE-001-coding-standard.md)
- [STD-API-001 — API Design Standard](../api/STD-API-001-api-design-standard.md)
- [STD-TEST-001 — Testing Standard](../testing/STD-TEST-001-testing-standard.md)
- [STD-DEP-001 — Dependency Management Standard](../dependency-management/STD-DEP-001-dependency-management-standard.md)
- [STD-DEPLOY-001 — Deployment Standard](../deployment/STD-DEPLOY-001-deployment-standard.md)
- [STD-OBS-001 — Observability Standard](../observability/STD-OBS-001-observability-standard.md)
- [STD-REL-001 — Release Management Standard](../release/STD-REL-001-release-management-standard.md)
- [STD-INC-001 — Incident Management Standard](../incident/STD-INC-001-incident-management-standard.md)
- [STD-RISK-001 — Enterprise Risk Management Standard](../risk/STD-RISK-001-enterprise-risk-management-standard.md)

## Related Playbooks

None. Future security playbook relationships remain planned until identified assets exist.

## References

- [Security Model](../../docs/architecture/SECURITY_MODEL.md)
- [Human-in-the-Loop Standard](../human-in-the-loop.md)
- [Dependency Management Standard](../dependency-management/STD-DEP-001-dependency-management-standard.md)

## Revision History

| Version | Date | Change | Author | Approval |
| --- | --- | --- | --- | --- |
| 0.4.0 | 2026-07-28 | Initial draft | Framework PMO | Pending Product Owner approval |
