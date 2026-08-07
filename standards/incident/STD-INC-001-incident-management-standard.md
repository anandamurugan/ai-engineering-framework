---
id: STD-INC-001
title: Incident Management Standard
version: 0.4.0
status: Draft
category: Incident Management
owner: Framework PMO
review_cycle: P12M
mandatory: true
ai_consumable: true
human_review_required: true
effective_date: null
last_reviewed: null
supersedes: []
related_standards:
  - STD-OBS-001
  - STD-SEC-001
  - STD-DEPLOY-001
  - STD-REL-001
  - STD-DOC-001
  - STD-RISK-001
related_playbooks: []
tags:
  - incident
  - reliability
  - operations
---

# STD-INC-001 – Incident Management Standard

## Purpose

Restore service safely, limit harm, communicate accurately, preserve evidence, learn from failure, and retain human accountability throughout incidents.

## Scope

Applies to operational, security, privacy, data, compliance, availability, performance, and delivery incidents affecting governed systems or stakeholders.

## Definitions

- **Incident Commander:** Authorized human accountable for coordination and incident decisions.
- **Severity:** Classification based on business, customer, security, data, regulatory, and operational impact.
- **Post-incident review:** Evidence-based analysis of causes, contributing factors, response, and improvements.

## Principles

Response is impact-led, role-based, time-conscious, evidence-preserving, communicative, blameless in learning, and governed by explicit human authority.

## Applicability

Suspected material impact MUST be assessed promptly under the approved incident policy. Uncertainty MUST NOT delay safe escalation.

## Mandatory Rules

1. **Lifecycle.** Incident processes MUST cover detection, initial assessment, declaration, classification, severity, triage, containment, mitigation, root-cause isolation, recovery, service restoration, validation, and authorized closure. Evidence: incident record and timeline.
2. **Severity.** Severity criteria MUST consider business, customer, security, privacy, data, regulatory, financial, and availability impact with defined escalation and response expectations. Evidence: severity decision and rationale.
3. **Roles.** Material incidents MUST assign an Incident Commander, Technical Lead, Communications Lead, operations or SRE role, and applicable security, business, product, or executive roles. Evidence: role assignment log.
4. **Authority.** Severity changes, destructive remediation, production access, external communication, regulatory notification, and closure MUST require authorized human decisions. Evidence: dated decision record.
5. **Detection and response.** Monitoring integrations, alert sources, automated detection, manual reporting, and event correlation MUST feed an owned triage process with an initial assessment, assigned Incident Commander, approved communication channel, and severity-based escalation procedure. Evidence: detection source inventory, alert or report, triage record, and role assignment.
6. **Containment and recovery.** Mitigation, containment, and recovery actions MUST state owner, expected impact, risk, authorization, result, and rollback where applicable; root-cause isolation and service restoration MUST be validated against technical and business criteria. Evidence: action and recovery log.
7. **Communication.** Internal status updates, executive updates, stakeholder notifications, customer communications, contractual notices, and regulatory updates MUST use approved channels, authorized senders, accurate known facts, uncertainty labels, and defined cadence. Evidence: communication log.
8. **Evidence preservation.** Incident documentation, timelines, decisions, actions, system and diagnostic evidence, communication records, change records, and failed attempts MUST form a protected audit trail retained according to policy and applicable obligations. Evidence: evidence inventory and retention configuration.
9. **Security involvement.** Suspected security, privacy, identity, supply-chain, or sensitive-data incidents MUST engage the authorized security response and notification process. Evidence: escalation record.
10. **Closure.** Closure MUST confirm stable recovery, SLA disposition, monitoring, stakeholder disposition, evidence completeness, follow-up ownership, and authorized approval. AI agents MUST NOT declare final closure. Evidence: closure checklist and approval.
11. **Post-incident review.** Material incidents MUST produce a root cause analysis that addresses causes, contributing factors, control gaps, response effectiveness, lessons learned, and systemic corrective and preventive actions without unsupported certainty. Evidence: approved RCA document.
12. **Knowledge and follow-up.** Actions MUST have owners, priority, due dates, validation, and traceability to corrective action plans, knowledge-base updates, runbooks, tests, standards, architecture, or problem-management updates. Evidence: corrective action register and updated knowledge references.
13. **Metrics.** Owners MUST monitor mean time to detect (MTTD), mean time to acknowledge (MTTA), mean time to recovery or resolve (MTTR), incident recurrence, SLA compliance, customer impact, communication performance, and corrective-action completion without gaming severity or suppressing incidents. Evidence: defined metrics and trend review.

## Recommended Practices

- Responders SHOULD use predefined channels, checklists, status formats, and decision logs.
- Post-incident reviews SHOULD distinguish triggering events, contributing conditions, detection gaps, and organizational factors.
- Exercises SHOULD test roles, communications, evidence, recovery, and escalation.

## Prohibited Practices or Anti-Patterns

- Responders MUST NOT conceal failed actions, alter historical evidence, blame individuals instead of analyzing systems, or delay escalation to protect metrics.
- AI agents MUST NOT change severity, send external messages, execute destructive remediation, or close incidents without human authorization.

## AI Implementation Guidance

AI agents MAY summarize incident timelines, correlate logs and alerts, recommend likely root causes, draft incident reports, generate RCA drafts, suggest corrective actions, retrieve knowledge, and recommend diagnostics within authorized access. Agents MUST label hypotheses, cite evidence, protect sensitive data, retain failed actions, and escalate uncertainty.

AI agents MUST NOT close incidents, approve RCA documents, declare service restoration, suppress critical alerts, override incident severity, approve production recovery, act as Incident Commander, or serve as the final accountable authority.

## Human Review Guidance

The Incident Commander governs response; technical and operations leads validate recovery; security leads govern security incidents; communications, business, product, legal, compliance, and executive reviewers participate according to impact. Authorized humans approve severity and closure.

## Required Evidence

- Incident record, declaration, severity decision, role assignments, timeline, decisions, actions, and owners
- System and diagnostic evidence, communication log, change and mitigation records, and failed-action history
- Recovery and business verification, root-cause analysis, corrective-action register, knowledge updates, and closure approval
- Metrics, review history, retention location, and linked security, release, deployment, or risk records

Evidence MUST be attributable, timestamped, protected, retainable, reviewable, and linked to the affected services and accountable roles.

## Validation Rules

- Automated checks SHOULD validate required incident fields, timestamps, role assignments, update cadence, open actions, and retention where tooling exists.
- Human review MUST verify severity, communication authority, evidence integrity, recovery, causal reasoning, follow-up adequacy, and closure approval.
- AI-generated summaries MUST be compared with source evidence before use in decisions or external communication.

## Exceptions

Incident urgency MAY change sequencing but MUST NOT eliminate human authority, evidence, security policy, or retrospective review. Exceptions follow the [Standards Review Process](../../docs/governance/STANDARD_REVIEW_PROCESS.md) and require scope, authority, risk, controls, expiry, and remediation.

## Related Standards

- [STD-OBS-001 — Observability Standard](../observability/STD-OBS-001-observability-standard.md)
- [STD-SEC-001 — Enterprise Security Standard](../security/STD-SEC-001-enterprise-security-standard.md)
- [STD-DEPLOY-001 — Deployment Standard](../deployment/STD-DEPLOY-001-deployment-standard.md)
- [STD-REL-001 — Release Management Standard](../release/STD-REL-001-release-management-standard.md)
- [STD-DOC-001 — Documentation Standard](../documentation/STD-DOC-001-documentation-standard.md)
- [STD-RISK-001 — Enterprise Risk Management Standard](../risk/STD-RISK-001-enterprise-risk-management-standard.md)

## Related Playbooks

None. Future incident playbook relationships remain planned until identified assets exist.

## References

- [Execution Model](../../docs/architecture/EXECUTION_MODEL.md)
- [Security Model](../../docs/architecture/SECURITY_MODEL.md)
- [Human-in-the-Loop Standard](../human-in-the-loop.md)

## Revision History

| Version | Date | Change | Author | Approval |
| --- | --- | --- | --- | --- |
| 0.4.0 | 2026-07-28 | Initial draft | Framework PMO | Pending Product Owner approval |
| 0.4.0 | 2026-08-07 | Clarified detection, response, communication, learning, metrics, evidence, and AI authority requirements | Framework PMO | Pending Product Owner approval |
