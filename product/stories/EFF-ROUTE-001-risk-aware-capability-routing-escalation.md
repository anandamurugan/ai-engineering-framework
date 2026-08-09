---
id: STORY-EFF-ROUTE-001
title: Deliver EFF-ROUTE-001 Risk-Aware Capability Routing & Escalation
version: 0.5.0
status: In Review
owner: Framework PMO
release: REL-005
epic: EPIC-002
sprint: SPR-005-003
priority: Critical
---

# STORY-EFF-ROUTE-001 – Risk-Aware Capability Routing & Escalation

## Business Value

Match execution capability to work while retaining transparent escalation and mandatory specialist authority for high-risk decisions.

## Problem Statement

Always using maximal capability wastes resources, while opaque low-capability routing or continuous escalation can weaken outcomes and accountability.

## Scope

Implement vendor-neutral conceptual tiers for deterministic or local tooling, lightweight AI, general engineering, advanced reasoning, and mandatory human or specialist decisions.

## Out of Scope

Vendor model names, price tables, automatic risk acceptance, or routing that bypasses required expertise.

## Requirements

- Routing MUST consider complexity, scope, security sensitivity, production impact, architectural significance, ambiguity, reversibility, reasoning depth, and tool requirements.
- The least-resource-intensive sufficient capability SHOULD be selected.
- Retry, context expansion, stronger capability, and human escalation MUST be bounded and evidence-based.
- Routing MUST record selected tier, considered dimensions, reason, escalation, and outcome.
- Humans retain authority for standards waivers, risk, exceptions, production, release, and mandatory reviews.

## Dependencies

[EFF-BUD-001](EFF-BUD-001-context-budgets-checkpoints-loop-controls.md), [EFF-CTX-001](EFF-CTX-001-execution-efficiency-context-management.md), and [SPR-005-003](../sprints/SPR-005-003-budgets-checkpoints-routing.md).

## Required Deliverable

[Execution Budgets, Checkpoints, and Routing](../../tools/execution/README.md), including generic Tier 1–5 policy, structured routing factors, deterministic recommendation and transition evidence, bounded failure escalation, de-escalation, and non-substitutable Tier 5 human authority.

## Acceptance Criteria

- Representative deterministic, low-risk, complex, sensitive, irreversible, and human-only work routes predictably.
- Escalation cannot grow capability or context indefinitely.
- Local or lightweight routing does not weaken privacy, security, quality, or validation.
- No normative artifact names a vendor-specific model.

## Validation Requirements

Test tier selection, escalation bounds, human-only gates, configuration, evidence, unavailable capability, failure, privacy, and vendor-neutrality cases.

## Definition of Ready

Tier semantics, risk dimensions, profile authority, evidence fields, and mandatory human gates are approved.

## Definition of Done

Routing is implemented, deterministic where defined, tested, documented, audited, validated, and human-reviewed.

Implementation, automated tests, documentation, and validation evidence are complete. Human review and Product Owner approval remain pending, so this story remains **In Review**.

## Product Owner Approval

Product Owner approval is required before this story is complete.
