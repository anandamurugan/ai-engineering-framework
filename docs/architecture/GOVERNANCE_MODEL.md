---
id: architecture.governance-model
title: Governance Model
version: 0.2.0
status: proposed
owner: Framework Maintainers
tags:
  - architecture
  - governance
  - human-authority
ai_consumable: true
human_reviewed: false
last_updated: 2026-07-23
---

# Governance Model

## Purpose

The governance model preserves accountable human authority while allowing bounded, evidence-producing agent participation. It complements the existing [risk classification](../../standards/risk-classification.md) and [human-in-the-loop](../../standards/human-in-the-loop.md) standards. Organizations may impose stricter controls.

## Governance principles

- Humans own business outcomes, policy, architecture, risk acceptance, access, and release decisions.
- Authority is explicit, scoped, time-bound where appropriate, and auditable.
- Agents cannot grant themselves approval or delegate authority they do not possess.
- Risk is classified by the highest credible impact and re-evaluated when facts change.
- Independent review and separation of duties increase with consequence and irreversibility.
- Evidence must support decisions; absence of evidence triggers a stop or escalation.
- Emergency pressure changes process timing, not accountability.

## Risk tiers

| Tier | Description | Minimum governance |
| --- | --- | --- |
| Low | Local, reversible, limited impact; no sensitive or production effect | Standard review and automated or manual checks |
| Moderate | Shared behavior or meaningful operational impact with understood recovery | Independent human review and targeted evidence |
| High | Production, sensitive data, security boundary, broad impact, or difficult rollback | Explicit human approval before execution and release; comprehensive evidence |
| Critical | Legal, safety, systemic, irreversible, or enterprise-wide impact | Designated authority, separation of duties, staged execution, recovery plan, and continuous oversight |

This architecture uses **Moderate** where the current standard uses **Medium**; they are equivalent until terminology is harmonized through a separately approved standards change.

## Authority matrix

| Decision | Agent | Authorized human |
| --- | --- | --- |
| Gather approved context | Perform within access | Define access boundary |
| Classify risk | Recommend with rationale | Confirm high or critical classification and controls |
| Create implementation plan | Propose | Approve when required |
| Make reversible in-scope implementation choices | Perform for low/moderate work | Review outcome |
| Change architecture or governance | Prohibited from approving | Approve through designated process |
| Accept security, privacy, compliance, or operational risk | Prohibited | Designated risk owner |
| Change production or perform destructive action | Prohibited without explicit authorization | Designated change authority |
| Release or merge | Prepare and recommend | Authorized reviewer or release authority |
| Grant identity, access, or credentials | Prohibited | Authorized identity/access owner |

## Required human approval gates

Explicit human approval is required:

1. when readiness depends on a material product, architecture, risk, or policy decision;
2. before high- or critical-risk execution;
3. before destructive, irreversible, production, identity, security-control, sensitive-data, or compliance-impacting action;
4. before accepting material residual risk or an exception;
5. before release or deployment where organizational policy requires authorization.

Approvals identify decision, scope, artifact or version, approver, conditions, and time. Approval for one stage does not imply approval for another.

## Mandatory stop conditions

An agent must stop the affected work and request human input for:

- destructive operations;
- production changes;
- security-control changes;
- identity and access changes;
- sensitive-data handling beyond established controls;
- schema changes with data-loss potential;
- irreversible migrations;
- compliance-impacting changes;
- unclear or conflicting requirements;
- insufficient test evidence.

The stop also applies when risk increases, credentials or permissions are missing, a safeguard fails, or observed state differs materially from the approved plan.

## Separation of duties

High and critical work must separate implementation from approval. The same agent must not author and independently approve a change. Human roles may be combined only when enterprise policy allows it and the resulting risk is explicitly accepted. Security, compliance, and release authorities retain independent veto or escalation rights within their mandates.

## Responsibility matrix

`A` = accountable decision owner, `R` = responsible contributor, `C` = consulted, `I` = informed, `—` = no default authority.

| Activity | Business owner | Product owner | Architect | Engineering lead | Security | Compliance | Release manager | Operations | AI agent |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Define business outcome | A | R | C | C | I | I | I | I | C |
| Approve scope and acceptance | C | A | C | R | I | I | I | I | C |
| Approve architecture | I | C | A | R | C | C | I | C | C |
| Approve implementation | I | C | C | A | C | I | I | C | R |
| Accept security risk | I | I | C | C | A | C | I | C | C |
| Accept compliance risk | C | I | C | I | C | A | I | I | C |
| Authorize release | I | C | I | C | C | C | A | R | C |
| Authorize production change | I | I | C | C | C | I | R | A | C |
| Execute bounded analysis | I | I | C | C | C | C | I | I | R |

Organizations assign named people to these responsibilities; the matrix does not create authority by itself.

## Evidence requirements

Evidence is proportionate to risk and includes applicable requirements, context sources, classification rationale, decisions, approvals, changes, tests, security and quality checks, artifact identity, rollback, monitoring, exceptions, and residual risks. Evidence must be attributable, tamper-evident where required, and retained according to enterprise policy.

## Escalation paths

Agents escalate first to the task owner or orchestrator, then to the accountable domain authority: product, architecture, engineering, security, compliance, release, or operations. If authorities conflict, pause the affected work and route the decision to the designated governance forum or executive risk owner. No agent resolves authority conflicts by choosing the least restrictive instruction.

## Emergency changes

Emergency processes may shorten consultation but still require a named incident or change authority, minimum necessary scope, recorded rationale, least privilege, verification, rollback consideration, and retrospective review. Emergency status never authorizes agents to self-approve.

## Policy exceptions

Exceptions must identify the policy, reason, scope, risk, compensating controls, owner, approver, start, expiry, and remediation plan. They are not precedent and must not be embedded silently in prompts or workflows.

## Auditability and decision ownership

Material actions and decisions must be traceable to an authenticated actor, approved scope, input context, artifact version, evidence, and outcome. The accountable human owns the decision even when an agent prepares the analysis.

## Conflict resolution

Enterprise law, regulation, security, and approved policy supersede repository content. Within the framework, use the [knowledge precedence model](KNOWLEDGE_MODEL.md#conflict-resolution-and-precedence). Unresolved ambiguity requires human adjudication and, for architecture or governance, an ADR or policy update.
