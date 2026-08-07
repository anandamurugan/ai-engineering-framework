---
id: STD-DEPLOY-001
title: Deployment Standard
version: 0.4.0
status: Draft
category: Deployment
owner: Framework PMO
review_cycle: P12M
mandatory: true
ai_consumable: true
human_review_required: true
effective_date: null
last_reviewed: null
supersedes: []
related_standards:
  - STD-GIT-001
  - STD-PR-001
  - STD-TEST-001
  - STD-DOC-001
  - STD-DEP-001
  - STD-SEC-001
  - STD-PERF-001
  - STD-OBS-001
  - STD-REL-001
  - STD-INC-001
  - STD-RISK-001
related_playbooks: []
tags:
  - deployment
  - delivery
  - operations
---

# STD-DEPLOY-001 – Deployment Standard

## Purpose

Make environment changes repeatable, traceable, secure, verifiable, and recoverable while preserving human authority over production.

## Scope

Applies to application, configuration, infrastructure, database, data, feature-control, and supporting-service changes promoted across governed environments.

## Definitions

- **Immutable artifact:** Versioned build output whose content cannot change under the same identity.
- **Progressive delivery:** Controlled exposure that expands only after defined verification.
- **Deployment record:** Traceable evidence of artifact, environment, approvals, actions, checks, outcome, and recovery.

## Principles

Build once, promote immutable artifacts, separate build from deployment, automate repeatable and consistent controls, preserve end-to-end traceability, use least privilege, make changes reversible, and require human production authority.

## Applicability

Every production change MUST use a governed deployment process. Risk determines strategy, approval depth, verification, and recovery evidence.

## Mandatory Rules

1. **Pipeline control.** Build and deployment processes MUST be repeatable, version-controlled, attributable, least-privileged, and separated by duty; production changes MUST NOT originate from unreviewed local actions. Evidence: pipeline definition and execution record.
2. **Artifact integrity.** Deployments MUST reference an immutable artifact with source revision, build evidence, dependency inventory, integrity verification, and approved repository location. Evidence: artifact digest and provenance.
3. **Configuration and secrets.** Environment-specific configuration MUST be externalized, versioned, validated, access-controlled, and separated from artifacts; deployments MUST use approved secret references, and secret values MUST be injected through approved mechanisms. Evidence: configuration version, validation result, and secret-control review.
4. **Infrastructure.** Material infrastructure MUST be managed as reviewed code where feasible, with environment consistency, drift detection, validation, ownership, and recovery. Evidence: infrastructure change and drift report.
5. **Environment separation.** Development, Integration, QA, UAT, and Production environments, or documented equivalents, MUST have defined purposes, access boundaries, data controls, promotion gates, and sufficient configuration consistency to validate the release candidate. Evidence: environment definition, comparison, and control record.
6. **Deployment readiness.** A release candidate MUST preserve identity across environments and have an approved change record, approved architecture where required, successful test results, security verification, required documentation, and validated rollback readiness before promotion. Evidence: readiness checklist and promotion record.
7. **Strategy.** Rolling, blue/green, canary, feature flags, progressive delivery, or another strategy MUST be selected from risk, compatibility, capacity, observability, and recovery needs. Evidence: deployment plan and rationale.
8. **Data changes.** Schema and data migrations MUST be validated for compatibility, duration, locking, data loss, backup, reconciliation, rollback or roll-forward, and interruption behavior. Irreversible or loss-capable changes MUST receive explicit human approval. Evidence: migration plan and rehearsal results.
9. **Deployment execution.** Approved artifacts, environment readiness, dependencies, capacity, security controls, observability, backups, recovery, and deployment windows MUST pass automated or recorded validation checkpoints before execution. Deployment automation MUST produce attributable logs of actions, actors, artifacts, environments, timestamps, validation results, and failures. Evidence: readiness checklist and deployment log.
10. **Post-deployment verification.** Smoke, health, security, telemetry, performance, and business checks appropriate to risk MUST execute after deployment with an accountable observation period. Failed checks MUST stop promotion or invoke the approved recovery decision. Evidence: smoke-test and post-deployment verification results.
11. **Recovery.** Every material deployment MUST define rollback criteria, documented rollback or roll-forward procedures, feature disablement where applicable, recovery-time and recovery-point objectives, failed-deployment escalation, and validation that recovery restored an acceptable state. Evidence: rollback plan, procedure, rehearsal, and validation result.
12. **Human controls.** An authorized human independent from sole implementation MUST approve the change record, production deployment, emergency changes, and exception use. Production authorization and segregation of duties MUST be recorded before execution. AI agents MUST NOT approve or initiate production deployment without that recorded gate. Evidence: change and deployment approval records.
13. **Operational metrics.** Owners MUST review deployment frequency, duration, verification success, change failure, rollback, recovery, and unauthorized-change rates without discouraging accurate failure reporting. Evidence: metric definitions and review.

## Recommended Practices

- Teams SHOULD prefer small, frequent, reversible changes and progressive exposure when risk warrants it.
- Database changes SHOULD use expand-and-contract patterns that preserve mixed-version compatibility.
- Pipeline identities SHOULD have short-lived credentials and environment-specific permissions.

## Prohibited Practices or Anti-Patterns

- Teams MUST NOT deploy mutable or unverified artifacts, bypass failed gates, embed secrets, conceal drift, or perform unrecorded production changes.
- Emergency status MUST NOT be used to avoid ownership, evidence, recovery, or retrospective review.

## AI Implementation Guidance

AI agents MAY prepare deployment documentation, verify deployment prerequisites, recommend deployment sequences, analyze deployment logs, summarize deployment results, and draft pipeline, migration, evidence, or recovery recommendations in authorized non-production scope. Agents MUST verify context, preserve failed evidence, disclose uncertainty, and stop for production, destructive, irreversible, sensitive-data, or unclear changes.

AI agents MUST NOT approve production deployments, bypass change management, authorize production changes, override deployment gates, suppress deployment failures, approve releases, or execute destructive recovery without authorization.

## Human Review Guidance

Engineering confirms artifact and implementation; QA confirms test evidence; security confirms controls; operations confirms environment, observation, and recovery; data owners approve migrations; the release authority makes the production decision. Product Owner approval remains required for this Draft.

## Required Evidence

- Deployment plan, immutable artifact reference, source revision, provenance, pipeline run, deployment logs, deployment approvals, change record, and release record
- Environment and configuration validation, infrastructure drift result, security and observability readiness
- Migration, backup, reconciliation, rollback or roll-forward plan and rehearsal evidence
- Smoke, health, business, post-deployment, monitoring, failure, incident, and metrics records

Evidence MUST identify owner, environment, artifact, time, decision, result, retention location, and linked release or incident.

## Validation Rules

- Automated checks SHOULD validate artifact identity, required gates, configuration, drift, migration checks, deployment outcome, and post-deployment signals where tooling exists.
- Human review MUST verify strategy, environment risk, migration safety, recovery feasibility, separation of duties, and production authority.
- Successful automation MUST NOT substitute for required human production approval.

## Exceptions

Exceptions follow the [Standards Review Process](../../docs/governance/STANDARD_REVIEW_PROCESS.md). Emergency deployment requires designated human authority, minimum safe evidence, incident or change reference, retrospective review, expiry, and remediation.

## Related Standards

- [STD-GIT-001 — Git and Branching Standard](../git/STD-GIT-001-git-and-branching-standard.md)
- [STD-PR-001 — Pull Request Standard](../pull-request/STD-PR-001-pull-request-standard.md)
- [STD-TEST-001 — Testing Standard](../testing/STD-TEST-001-testing-standard.md)
- [STD-DOC-001 — Documentation Standard](../documentation/STD-DOC-001-documentation-standard.md)
- [STD-DEP-001 — Dependency Management Standard](../dependency-management/STD-DEP-001-dependency-management-standard.md)
- [STD-SEC-001 — Enterprise Security Standard](../security/STD-SEC-001-enterprise-security-standard.md)
- [STD-PERF-001 — Performance and Scalability Standard](../performance/STD-PERF-001-performance-scalability-standard.md)
- [STD-OBS-001 — Observability Standard](../observability/STD-OBS-001-observability-standard.md)
- [STD-REL-001 — Release Management Standard](../release/STD-REL-001-release-management-standard.md)
- [STD-INC-001 — Incident Management Standard](../incident/STD-INC-001-incident-management-standard.md)
- [STD-RISK-001 — Enterprise Risk Management Standard](../risk/STD-RISK-001-enterprise-risk-management-standard.md)

## Related Playbooks

None. Future deployment playbook relationships remain planned until identified assets exist.

## References

- [Execution Model](../../docs/architecture/EXECUTION_MODEL.md)
- [Release Model](../../docs/architecture/RELEASE_MODEL.md)
- [Human-in-the-Loop Standard](../human-in-the-loop.md)

## Revision History

| Version | Date | Change | Author | Approval |
| --- | --- | --- | --- | --- |
| 0.4.0 | 2026-07-28 | Initial draft | Framework PMO | Pending Product Owner approval |
| 0.4.0 | 2026-08-07 | Clarified readiness, environment, configuration, execution, rollback, evidence, and AI governance requirements | Framework PMO | Pending Product Owner approval |
