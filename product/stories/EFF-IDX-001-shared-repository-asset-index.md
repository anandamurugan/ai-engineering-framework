---
id: STORY-EFF-IDX-001
title: Deliver EFF-IDX-001 Shared Repository Asset Index
version: 0.5.0
status: Proposed
owner: Framework PMO
release: REL-005
epic: EPIC-002
sprint: SPR-005-002
priority: Critical
---

# STORY-EFF-IDX-001 – Shared Repository Asset Index

## Business Value

Reduce repeated scans and support reliable context and validation scoping through one reproducible view of repository assets.

## Problem Statement

Independent full-repository discovery duplicates work and makes selection, dependency impact, and evidence counts inconsistent.

## Scope

Design and implement a derived immutable-per-run index for asset ID, type, path, relationships, applicable standards, dependencies, lifecycle, change state, and validation scope.

## Out of Scope

Replacing repository sources of truth, remote indexing products, semantic search vendors, or automatic approval.

## Requirements

- The index MUST be reproducible from a named repository revision and MUST NOT become authoritative over source artifacts.
- Consumers MUST detect stale, incomplete, unsupported, or ambiguous index state and fall back safely.
- Index construction MUST honor repository exclusions and sensitive-path authorization.
- Provenance, freshness, errors, and scan counts MUST be observable.
- The format SHOULD support future asset types without a core redesign.

## Dependencies

[EFF-CTX-001](EFF-CTX-001-execution-efficiency-context-management.md), [EFF-MET-001](EFF-MET-001-efficiency-measurement-evidence-contract.md), and [SPR-005-002](../sprints/SPR-005-002-repository-index-targeted-context.md).

## Required Deliverable

A repository-conforming index contract and implementation with tests, evidence, documentation, and safe fallback behavior.

## Acceptance Criteria

- Representative assets and relationships are indexed deterministically.
- A run uses one immutable index snapshot with source revision evidence.
- Stale or incomplete state is detected and cannot silently narrow required work.
- Repeated-scan reduction is measurable without hiding actual source coverage.

## Validation Requirements

Test determinism, uniqueness, freshness, exclusions, sensitive paths, malformed inputs, resource bounds, and fallback.

## Definition of Ready

Index consumers, authoritative sources, schema, lifecycle, exclusion, security, and fallback contracts are approved.

## Definition of Done

The index implementation, tests, documentation, evidence, validation, and human review satisfy the story contract.

## Product Owner Approval

Product Owner approval is required before this story is complete.
