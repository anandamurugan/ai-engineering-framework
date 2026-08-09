---
id: STORY-EFF-MET-001
title: Deliver EFF-MET-001 Efficiency Measurement & Evidence Contract
version: 0.5.0
status: Proposed
owner: Framework PMO
release: REL-005
epic: EPIC-002
sprint: SPR-005-001
priority: High
---

# STORY-EFF-MET-001 – Efficiency Measurement & Evidence Contract

## Business Value

Make optimization decisions comparable and auditable on platforms with or without token telemetry.

## Problem Statement

Token-only measures omit retrieval, repeated scans, time, retries, tools, capability cost, reuse, validation scope, and quality consequences.

## Scope

Define shared terminology, measurement semantics, provenance, and quality safeguards for execution-efficiency evidence.

## Out of Scope

Universal targets, vendor billing data, leaderboards, or metrics that reward unsafe under-contexting.

## Requirements

- Evidence SHOULD capture files, bytes, retrievals, invocations, duration, retries, failed attempts, tool calls, validation scope, capability tier, reuse, and tokens when available.
- Counts MUST define their unit, scope, source state, and unavailable-value behavior.
- Relevant-context and efficiency measures MUST be paired with quality, validation, security, privacy, and governance outcomes.
- Routing, expansion, fallback, and escalation decisions MUST be attributable.
- Evidence MUST remain distinct from review, approval, and risk acceptance.

## Dependencies

[EFF-CTX-001](EFF-CTX-001-execution-efficiency-context-management.md) and [SPR-005-001](../sprints/SPR-005-001-release-architecture-efficiency-contracts.md).

## Required Deliverable

A shared efficiency measurement and evidence contract suitable for later checkpoints, routing, indexing, and validation reports.

## Acceptance Criteria

- Every named metric has a definition and an unavailable-data behavior.
- Exact token counts are optional.
- Measurements cannot represent failed quality or governance as successful efficiency.
- Evidence provenance supports review and later machine-readable implementation.

## Validation Requirements

Review definitions for measurability, vendor neutrality, non-duplication, provenance, privacy, and traceability.

## Definition of Ready

Consumers, authoritative terminology, platform-neutral fields, and governance limitations are identified.

## Definition of Done

The contract is reviewed, validated, traceable, and ready for implementation stories.

## Product Owner Approval

Product Owner approval is required before this story is complete.
