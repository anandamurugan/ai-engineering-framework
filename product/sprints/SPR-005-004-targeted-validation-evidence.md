---
id: SPR-005-004
title: Sprint 5.4 - Targeted Validation & Evidence Provenance
version: 0.5.0
status: Planned
owner: Framework PMO
release: REL-005
epic: EPIC-002
---

# SPR-005-004 – Targeted Validation & Evidence Provenance

## Objective

Add safe targeted and changed-file validation, affected dependency closure, richer evidence provenance, and resource-bound validator behavior.

## Scope

### Included

- Specific-asset, changed-file, affected-closure, and full-validation execution modes
- Deterministic fallback for ambiguous impact, stale indexing, governance-sensitive changes, and release validation
- Product metadata contracts, registry integrity, exception-path tests, evidence provenance, scan semantics, and resource bounds

### Excluded

- Validation suppression, automatic remediation, human approval, dedicated Markdown linting, or secret-scanning implementation

## Stories

| Story | Planned deliverable |
| --- | --- |
| [EFF-VAL-001](../stories/EFF-VAL-001-targeted-validation-evidence-provenance.md) | Targeted/Changed-File Validation & Evidence Provenance |

## Dependencies

- [SPR-005-002](SPR-005-002-repository-index-targeted-context.md)
- [SPR-005-003](SPR-005-003-budgets-checkpoints-routing.md)

## Acceptance Criteria

- A change cannot escape required validation because its impact is unknown or unsupported.
- Reports identify source revision, selection mode, included files, affected closure, exclusions, fallback reason, validator set, and unambiguous scan counts.
- Full validation remains available and mandatory for defined release, governance, ambiguity, and index-integrity conditions.
- Existing full validation behavior remains compatible and all tests pass.

## Definition of Done

EFF-VAL-001 is complete, targeted and full paths are tested, provenance is reviewable, and repository validation passes without reclassifying findings.
