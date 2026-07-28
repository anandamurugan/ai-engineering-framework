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

Suspected material impact MUST be assessed promptly under the organization’s incident process. Uncertainty MUST NOT delay safe escalation.

## Mandatory Rules

1. **Lifecycle.** Incident processes MUST cover detection, declaration, classification, severity, triage, containment, mitigation, recovery, validation, and authorized closure. Evidence: incident record and timeline.
2. **Severity.** Severity criteria MUST consider business, customer, security, privacy, data, regulatory, financial, and availability impact with defined escalation and response expectations. Evidence: severity decision and rationale.
3. **Roles.** Material incidents MUST assign an Incident Commander, Technical Lead, Communications Lead, operations or SRE role, and applicable security, business, product, or executive roles. Evidence: role assignment log.
4. **Authority.** Severity changes, destructive remediation, production access, external communication, regulatory notification, and closure MUST require authorized human decisions. Evidence: dated decision record.
5. **Containment and recovery.** Actions MUST state owner, expected impact, risk, authorization, result, and rollback where applicable; recovery MUST be validated against technical and business criteria. Evidence: action and recovery log.
6. **Communication.** Internal, customer, executive, contractual, and regulatory updates MUST use approved channels, authorized senders, accurate known facts, uncertainty labels, and defined cadence. Evidence: communication log.
7. **Evidence preservation.** Timelines, decisions, actions, system and diagnostic evidence, change records, and failed attempts MUST be preserved with access and retention controls. Evidence: evidence inventory.
8. **Security involvement.** Suspected security, privacy, identity, supply-chain, or sensitive-data incidents MUST engage the authorized security response and notification process. Evidence: escalation record.
9. **Closure.** Closure MUST confirm stable recovery, monitoring, stakeholder disposition, evidence completeness, follow-up ownership, and authorized approval. AI agents MUST NOT declare final closure. Evidence: closure checklist and approval.
10. **Post-incident review.** Material incidents MUST analyze root causes, contributing factors, control gaps, response effectiveness, and systemic corrective and preventive actions without unsupported certainty. Evidence: approved review.
11. **Knowledge and follow-up.** Actions MUST have owners, priority, due dates, validation, and traceability to runbook, test, standard, architecture, or problem-management updates. Evidence: action register.
12. **Metrics.** Owners MUST monitor time to acknowledge, mitigate, recover, repeat-incident rate, communication performance, and corrective-action completion without gaming severity or suppressing incidents. Evidence: defined metrics and trend review.

## Recommended Practices

- Responders SHOULD use predefined channels, checklists, status formats, and decision logs.
- Post-incident reviews SHOULD distinguish triggering events, contributing conditions, detection gaps, and organizational factors.
- Exercises SHOULD test roles, communications, evidence, recovery, and escalation.

## Prohibited Practices or Anti-Patterns

- Responders MUST NOT conceal failed actions, alter historical evidence, blame individuals instead of analyzing systems, or delay escalation to protect metrics.
- AI agents MUST NOT change severity, send external messages, execute destructive remediation, or close incidents without human authorization.

## AI Implementation Guidance

AI agents MAY correlate events, retrieve knowledge, draft timelines and summaries, generate hypotheses, and recommend diagnostics within authorized access. Agents MUST label hypotheses, cite evidence, protect sensitive data, retain failed actions, and escalate uncertainty. Agents cannot act as Incident Commander or final accountable authority.

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
