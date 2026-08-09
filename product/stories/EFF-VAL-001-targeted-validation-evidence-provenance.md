---
id: STORY-EFF-VAL-001
title: Deliver EFF-VAL-001 Targeted Validation & Evidence Provenance
version: 0.5.0
status: Proposed
owner: Framework PMO
release: REL-005
epic: EPIC-002
sprint: SPR-005-004
priority: Critical
---

# STORY-EFF-VAL-001 – Targeted Validation & Evidence Provenance

## Business Value

Reduce unnecessary validation work while proving that every affected governed asset still receives required checks.

## Problem Statement

Full scans are safe but increasingly repetitive; naive changed-file validation can miss dependencies, weaken release evidence, or produce ambiguous coverage counts.

## Scope

Implement specific-asset, changed-file, affected-closure, and full-validation modes plus product metadata contracts, registry integrity, exception tests, provenance, scan semantics, and resource bounds.

## Out of Scope

Suppression, auto-fixing, approval, dedicated Markdown linter, secret scanner, or replacement of full release validation.

## Requirements

- Affected closure MUST use governed relationships and MUST fall back to full validation when completeness is uncertain.
- Full validation MUST remain mandatory for release gates and other repository-defined sensitive changes.
- Evidence MUST identify revision, selection mode, requested and expanded assets, exclusions, fallback, validators, results, and unambiguous counts.
- Registry IDs MUST be unique and validator exceptions MUST become visible failures.
- Resource limits MUST fail safely without representing incomplete execution as PASS.

## Dependencies

[EFF-IDX-001](EFF-IDX-001-shared-repository-asset-index.md), [EFF-SEL-001](EFF-SEL-001-progressive-targeted-context-selection.md), and [SPR-005-004](../sprints/SPR-005-004-targeted-validation-evidence.md).

## Required Deliverable

Compatible validation-framework enhancements, executable product contracts, tests, JSON evidence, and operational documentation.

## Acceptance Criteria

- Targeted, changed-file, affected-closure, and full modes produce correct scope for fixtures and repository changes.
- Ambiguity, stale index, unsupported asset, governance-sensitive change, and release execution select full validation.
- Existing validation results and exit semantics remain compatible.
- ARCH-REL004-002, ARCH-REL004-003, ARCH-REL004-004, ARCH-REL004-006, SEC-REL004-005, and SEC-REL004-006 have evidence-backed disposition.

## Validation Requirements

Run existing and new tests for closure, fallback, provenance, counts, exceptions, registry uniqueness, resource bounds, JSON output, and full-run compatibility.

## Definition of Ready

Index, relationship authority, selection policy, product contracts, fallback rules, provenance semantics, and compatibility expectations are approved.

## Definition of Done

The enhancements pass complete and targeted validation, tests, CI, documentation review, security review, and Product Owner approval.

## Product Owner Approval

Product Owner approval is required before this story is complete.
