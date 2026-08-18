---
id: EPIC-002
title: Efficient Agentic Execution & Context Engineering
version: 0.5.0
status: Completed
owner: Framework PMO
release: REL-005
priority: Critical
---

# EPIC-002 – Efficient Agentic Execution & Context Engineering

## Vision

Enable bounded AI-assisted engineering execution that selects only justified context and capability, preserves durable evidence, and escalates safely under accountable human governance.

## Business Value

- Reduce repeated repository scanning and irrelevant context loading.
- Improve execution predictability, resumability, and auditability.
- Apply capable resources proportionately without trading away quality or safety.
- Make routing, retry, validation-scope, and escalation decisions reviewable.
- Preserve vendor neutrality across deterministic tools, local engines, hosted agents, and future platforms.

## Objectives

- Define EFF-CTX-001 as the primary governed execution-efficiency capability.
- Establish platform-neutral measurement and evidence contracts.
- Provide an immutable repository asset index and targeted context-selection design.
- Govern configurable budgets, checkpoints, retries, loop response, routing, and escalation.
- Extend validation toward changed-file and affected-closure execution with safe full-scan fallback.
- Close the release through validation and separate human review.

## Scope

### Included

- Eight planned product stories across five incremental sprints
- Context minimization, progressive loading, task isolation, durable reuse, and context hygiene
- Risk-aware capability routing, bounded retry, checkpointing, and escalation evidence
- Repository indexing, targeted validation, provenance, measurement, and selected v0.4 follow-up

### Out of Scope

- Vendor-specific agent or model integrations
- Playbook, workflow, agent, or prompt catalogs
- Automatic approval, risk acceptance, release, deployment, or validation suppression
- v0.4 history changes or Draft-standard promotion

## Success Metrics

- Context-selection evidence identifies initial files, expansions, justification, and applicable exclusions.
- Measurement covers files, bytes, retrievals, invocations, time, retries, tools, validation scope, tiers, and reuse; token use is optional.
- Equivalent failures trigger bounded reassessment, escalation, human input, or termination.
- Targeted validation proves affected closure or selects full validation.
- Checkpoint-resume exercises retain required state without replaying full conversation history.
- Every efficiency result is evaluated with quality, security, privacy, and governance outcomes.

## Sprint Breakdown

| Sprint ID | Sprint | Goal | Progress |
| --- | --- | --- | --- |
| [SPR-005-001](../sprints/SPR-005-001-release-architecture-efficiency-contracts.md) | Sprint 5.1 | Release Architecture, Requirements & Efficiency Contracts | Completed |
| [SPR-005-002](../sprints/SPR-005-002-repository-index-targeted-context.md) | Sprint 5.2 | Repository Index & Targeted Context | Completed |
| [SPR-005-003](../sprints/SPR-005-003-budgets-checkpoints-routing.md) | Sprint 5.3 | Budgets, Checkpoints & Routing | Completed |
| [SPR-005-004](../sprints/SPR-005-004-targeted-validation-evidence.md) | Sprint 5.4 | Targeted Validation & Evidence Provenance | Completed |
| [SPR-005-005](../sprints/SPR-005-005-governance-release-closeout.md) | Sprint 5.5 | Governance Validation & Release Closeout | Completed |

## Dependencies

- [REL-005](../releases/REL-v0.5.md)
- Released v0.4.0 standards, governance, validation, and traceability foundations
- Existing repository asset taxonomy and validation framework

## Key Risks

- Efficiency targets encourage insufficient context.
- Capability tiers become proxies for particular vendors.
- Shared indexes become stale or authoritative beyond source assets.
- Targeted validation omits indirect impact.
- Checkpoints or automated evidence are treated as approvals.

## Risk Controls

- Give quality and governance precedence over efficiency.
- Require attributable selection, expansion, routing, retry, and fallback evidence.
- Treat indexes as derived immutable views with freshness and full-scan fallback.
- Keep approval and risk decisions with authorized humans.
- Validate normative content for vendor-specific coupling.

## Definition of Done

- All five sprints and eight stories are complete and traceable.
- Planned contracts, implementation, tests, documentation, and evidence pass governed validation.
- Included v0.4 findings have explicit disposition.
- Required human reviews and Product Owner approval are recorded separately from automated PASS results.

## Completion Record

All eight EFF stories are **Done**, all five sprints are **Completed**, and the authorized Product Owner decision accepts EPIC-002 as **Completed**. Documented non-blocking debt and accepted residual risks remain visible. REL-005 release authorization and tagging remain separate controls.
