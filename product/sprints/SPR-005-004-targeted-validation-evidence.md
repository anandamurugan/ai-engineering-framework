---
id: SPR-005-004
title: Sprint 5.4 - Targeted Validation & Evidence Provenance
version: 0.5.0
status: Completed
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

## Implementation Evidence

- The existing validation command supports full, targeted-asset, changed-file, and affected-closure modes without creating a second runner.
- Git change discovery uses fixed argument arrays and records base/head revisions, changed paths, ignored paths, and unresolved inputs.
- The Sprint 5.2 RepositoryView maps governed changes and expands authoritative forward and reverse relationships; uncertainty and governance-sensitive changes fall back to full validation.
- Targetable validators receive affected paths while repository-wide validators retain global integrity coverage.
- Registry integrity and validator exception paths fail deterministically with structured evidence.
- JSON report format 2.0 records repository and runtime provenance, modes, scope, closure, fallback, validator IDs, policy fingerprint, results, and explicit scan-count semantics.
- Full validation remains the CI and REL-005 release-gate default.
- EFF-VAL-001 is **Done** under the authorized Product Owner decision.
- Implementation status: **Complete**. Human approval status: **Approved**. Sprint status: **Completed**.

## Carried Findings

| Finding | Sprint 5.4 disposition |
| --- | --- |
| ARCH-REL004-003 | Addressed by versioned provenance and explicit governed/scoped/affected/check/finding count semantics. Final closure remains subject to review. |
| ARCH-REL004-004 | Addressed by registry identity/uniqueness checks and focused exception-to-error tests. Final closure remains subject to review. |
| ARCH-REL004-006 | Progressed through RepositoryView reuse for affected planning and framework-ID integrity. Broader validator read consolidation remains a measured future optimization. |
| SEC-REL004-005 | Addressed proportionately through revision, time, runtime, validator-set, mode, scope, fallback, and policy-fingerprint evidence. Cryptographic signing remains out of scope. |
