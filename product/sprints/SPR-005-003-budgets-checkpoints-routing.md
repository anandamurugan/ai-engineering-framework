---
id: SPR-005-003
title: Sprint 5.3 - Budgets, Checkpoints & Routing
version: 0.5.0
status: In Review
owner: Framework PMO
release: REL-005
epic: EPIC-002
---

# SPR-005-003 – Budgets, Checkpoints & Routing

## Objective

Govern configurable execution budgets, durable checkpoints, bounded retry and loop response, and risk-aware capability routing.

## Scope

### Included

- Profile-configurable budgets for initial files, context, expansion, retries, failures, duration, and tool invocations
- Structured checkpoints for state, decisions, validation, findings, next action, and escalation
- Conceptual capability tiers, routing dimensions, escalation evidence, stop conditions, and mandatory human decisions

### Excluded

- Universal numeric thresholds, vendor model catalogs, price optimization, or automatic governance decisions

## Stories

| Story | Planned deliverable |
| --- | --- |
| [EFF-BUD-001](../stories/EFF-BUD-001-context-budgets-checkpoints-loop-controls.md) | Context Budgets, Checkpoints & Loop Controls |
| [EFF-ROUTE-001](../stories/EFF-ROUTE-001-risk-aware-capability-routing-escalation.md) | Risk-Aware Capability Routing & Escalation |

## Dependencies

- [SPR-005-001](SPR-005-001-release-architecture-efficiency-contracts.md)
- [SPR-005-002](SPR-005-002-repository-index-targeted-context.md)

## Acceptance Criteria

- Budget exceedance yields stop, reassessment, justified expansion, capability escalation, or human input rather than silent continuation.
- Equivalent failure, unsuccessful patch, dependency failure, unchanged test failure, oscillation, and unproductive expansion patterns are bounded.
- Routing uses task complexity, scope, sensitivity, impact, significance, ambiguity, reversibility, reasoning, and tool requirements.
- Checkpoints support resume without becoming approval records or containing unnecessary sensitive context.

## Definition of Done

Both stories are complete, failure and resumption paths are tested, and automated choices remain reviewable recommendations within human authority boundaries.

## Implementation Evidence

- [Execution Budgets, Checkpoints, and Routing](../../tools/execution/README.md) documents budget dimensions, caller-supplied profiles, threshold actions, state evaluation, checkpoint provenance and authority, loop signatures, routing policy, evidence, commands, security, anti-gaming controls, and limitations.
- `tools.execution` consumes Sprint 5.2 context-manifest counts and restriction/fallback state without rebuilding the index or selector.
- Configurable budgets distinguish unavailable telemetry from zero and never remove required context or controls.
- JSON checkpoints preserve budget, retry, loop, routing, escalation, and restricted-context state; incompatible repository commits require revalidation.
- Generic Tier 1–5 routing returns evidence-backed recommendations only. Tier 5 remains accountable human or specialist authority and cannot be replaced by Tier 4.
- Focused standard-library tests cover budget boundaries, optional telemetry, checkpoint round trips and staleness, normalized loop signatures and responses, tier selection, escalation, de-escalation, and human-only decisions.
- EFF-BUD-001 and EFF-ROUTE-001 are **In Review**. Sprint 5.3 is not complete until human review and Product Owner approval are recorded.

## Carried Findings

| Finding | Sprint 5.3 disposition |
| --- | --- |
| ARCH-REL004-004 | Partially addressed through explicit failure-path tests for budget, checkpoint, loop, and routing controls. Validation-registry uniqueness and validator-specific exception coverage remain assigned to EFF-VAL-001 in Sprint 5.4. |
| SEC-REL004-006 | Materially addressed for the Sprint 5.3 layer through configurable resource thresholds, bounded retries and equivalent failures, safe stop/human responses, minimal hashed signatures, and checkpoint compatibility checks. Broader validator resource bounds remain assigned to EFF-VAL-001. |
