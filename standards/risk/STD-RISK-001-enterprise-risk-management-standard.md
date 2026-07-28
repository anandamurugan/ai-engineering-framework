---
id: STD-RISK-001
title: Enterprise Risk Management Standard
version: 0.4.0
status: Draft
category: Risk Management
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
  - STD-SEC-001
  - STD-PERF-001
  - STD-OBS-001
  - STD-DEPLOY-001
  - STD-REL-001
  - STD-INC-001
related_playbooks: []
tags:
  - risk
  - governance
  - compliance
---

# STD-RISK-001 – Enterprise Risk Management Standard

## Purpose

Make engineering risk visible, consistently assessed, owned, treated, monitored, escalated, and accepted only by authorized humans.

## Scope

Applies to architecture, technical, security, privacy, delivery, operational, performance, availability, compliance, third-party, supply-chain, data, and AI-specific risk.

## Definitions

- **Inherent risk:** Risk before considering controls.
- **Residual risk:** Risk remaining after controls and treatment.
- **Risk acceptance:** Time-bound human decision to retain residual risk within documented authority.

## Principles

Risk management is evidence-based, proportional, continuous, transparent, owned, time-bounded, integrated with delivery, and independent from AI-generated approval.

## Applicability

Material engineering decisions and changes MUST identify and manage applicable risk. The highest credible impact determines required escalation and authority.

## Mandatory Rules

1. **Risk identification.** Risks MUST state cause, uncertain event, impact, affected assets, stakeholders, assumptions, evidence, and applicable domain. Evidence: risk record.
2. **Coverage.** Reviews MUST consider architecture, technical, security, privacy, delivery, operational, performance, availability, compliance, third-party, supply-chain, data, and AI-specific risk. Evidence: risk checklist and rationale for exclusions.
3. **Assessment.** Each material risk MUST record likelihood, impact, inherent rating, control effectiveness, residual rating, time horizon, dependency risk, and assessment rationale using an approved method. Evidence: assessment record.
4. **Ownership.** Every material risk MUST have an accountable human owner with authority to coordinate treatment and escalation. AI agents MUST NOT own or accept risk. Evidence: risk register.
5. **Treatment.** Risks MUST use an explicit avoid, reduce, transfer, accept, or escalate decision with mitigation actions, owners, target dates, dependencies, contingency, and validation. Evidence: treatment plan.
6. **Controls.** Control design and operation MUST be assessed separately, with failed, missing, or untested controls reflected in residual risk. Evidence: control assessment.
7. **Acceptance.** Risk acceptance MUST identify authorized approver, rationale, scope, residual exposure, compensating controls, review date, expiry, and revocation conditions. Evidence: approval record.
8. **Escalation.** High, critical, overdue, worsening, cross-domain, or authority-exceeding risks MUST be escalated according to defined thresholds before affected approval gates. Evidence: escalation record.
9. **Review cadence.** Risks MUST be reviewed at an interval based on severity and when material changes, incidents, findings, dependencies, or control failures occur. Evidence: review history.
10. **Closure.** A risk MUST NOT close until treatment and control evidence are verified, residual risk is within authority, dependencies are resolved, and an authorized human approves closure. Evidence: closure record.
11. **Auditability.** Risk register changes, scores, decisions, owners, evidence, approvals, expiries, and history MUST be retained and attributable. Evidence: auditable register history.
12. **Metrics.** Owners MUST monitor open high risks, overdue mitigations, accepted-risk age, risk trend, expired acceptances, and control effectiveness without lowering scores or hiding risks to improve reporting. Evidence: metric definitions and review.
13. **AI governance.** AI-related risks MUST address data, access, prompt injection, inaccurate output, automation bias, model or vendor dependency, evidence integrity, and excessive autonomy where applicable. Evidence: AI risk assessment.

## Recommended Practices

- Teams SHOULD express risks in a consistent cause-event-impact format and use scenarios to test assumptions.
- Risk registers SHOULD link directly to requirements, controls, incidents, decisions, and treatment evidence.
- Independent challenge SHOULD be used for high-impact assessments and acceptances.

## Prohibited Practices or Anti-Patterns

- Teams MUST NOT treat missing evidence as proof of low risk, accept risk without authority, use permanent unreviewed acceptance, or close risk solely because a target date passed.
- AI agents MUST NOT lower scores, accept or close risk, override controls, or conceal unresolved exposure.

## AI Implementation Guidance

AI agents MAY discover risks, collect authorized evidence, draft statements, analyze scenarios, suggest ratings and mitigations, and identify trends. Agents MUST cite sources, expose uncertainty and conflicting evidence, avoid fabricated precision, and escalate authority gaps. All ratings, treatment, acceptance, and closure decisions require accountable human review.

## Human Review Guidance

Risk owners maintain records and treatment; domain reviewers assess controls; security, privacy, compliance, architecture, operations, and business authorities review applicable impacts. Only designated humans accept residual risk, and Product Owner approval remains required for this standard.

## Required Evidence

- Risk statement, affected assets, assumptions, sources, assessment rationale, inherent and residual ratings
- Control assessment, treatment and contingency plan, owners, due dates, dependencies, and validation
- Acceptance or escalation approval, scope, expiry, review history, metrics, and audit trail
- Closure evidence, independent review where required, and links to incidents, standards, decisions, and corrective actions

Evidence MUST be named, attributable, traceable, retainable, reviewable, and associated with an accountable human role.

## Validation Rules

- Automated checks SHOULD detect missing owners, evidence, reviews, overdue actions, expired acceptances, and inconsistent rating fields where tooling exists.
- Human review MUST assess scenario completeness, rating rationale, control effectiveness, treatment feasibility, authority, and closure evidence.
- Automated scoring MUST NOT confer acceptance or override human-governed risk thresholds.

## Exceptions

Exceptions to risk-process requirements follow the [Standards Review Process](../../docs/governance/STANDARD_REVIEW_PROCESS.md) and MUST NOT be used to bypass risk acceptance authority. Requests require scope, rationale, risk, controls, owner, approver, expiry, monitoring, and remediation.

## Related Standards

- [STD-ARCH-001 — Architecture Standard](../architecture/STD-ARCH-001-architecture-standard.md)
- [STD-SEC-001 — Enterprise Security Standard](../security/STD-SEC-001-enterprise-security-standard.md)
- [STD-PERF-001 — Performance and Scalability Standard](../performance/STD-PERF-001-performance-scalability-standard.md)
- [STD-OBS-001 — Observability Standard](../observability/STD-OBS-001-observability-standard.md)
- [STD-DEPLOY-001 — Deployment Standard](../deployment/STD-DEPLOY-001-deployment-standard.md)
- [STD-REL-001 — Release Management Standard](../release/STD-REL-001-release-management-standard.md)
- [STD-INC-001 — Incident Management Standard](../incident/STD-INC-001-incident-management-standard.md)

## Related Playbooks

None. Future risk playbook relationships remain planned until identified assets exist.

## References

- [Risk Classification Standard](../risk-classification.md)
- [Governance Model](../../docs/architecture/GOVERNANCE_MODEL.md)
- [Human-in-the-Loop Standard](../human-in-the-loop.md)

## Revision History

| Version | Date | Change | Author | Approval |
| --- | --- | --- | --- | --- |
| 0.4.0 | 2026-07-28 | Initial draft | Framework PMO | Pending Product Owner approval |
