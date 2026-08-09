---
id: SPR-005-002
title: Sprint 5.2 - Repository Index & Targeted Context
version: 0.5.0
status: In Review
owner: Framework PMO
release: REL-005
epic: EPIC-002
---

# SPR-005-002 – Repository Index & Targeted Context

## Objective

Provide derived repository knowledge and deterministic selection behavior that reduce repeated scans while preserving complete, auditable context expansion.

## Scope

### Included

- Immutable derived asset index for identity, type, path, relationships, standards, dependencies, lifecycle, change state, and validation scope
- Progressive selection from product contract to standards, targets, direct dependencies, and justified wider context
- Index freshness, exclusion, sensitive-path, authorization, and full-scan fallback rules

### Excluded

- Index as a replacement for authoritative repository artifacts
- Remote knowledge services, embeddings, vendor retrieval products, or autonomous approval

## Stories

| Story | Planned deliverable |
| --- | --- |
| [EFF-IDX-001](../stories/EFF-IDX-001-shared-repository-asset-index.md) | Shared Repository Asset Index |
| [EFF-SEL-001](../stories/EFF-SEL-001-progressive-targeted-context-selection.md) | Progressive & Targeted Context Selection |

## Dependencies

- [SPR-005-001](SPR-005-001-release-architecture-efficiency-contracts.md)
- [EPIC-002](../epics/EPIC-002-efficient-agentic-execution-context-engineering.md)

## Acceptance Criteria

- Index records are reproducible, immutable for a run, attributable to source state, and never supersede source artifacts.
- Selection evidence records included, excluded, expanded, and sensitive context with justification.
- Stale, incomplete, ambiguous, security-sensitive, or unsupported index states trigger safe fallback.
- Tests demonstrate relevant selection, dependency expansion, exclusions, authorization, and fallback.

## Definition of Done

Both stories meet their Definitions of Done, validation passes, and human review confirms that reduced scanning cannot bypass required context or governance.

## Implementation Evidence

- [Repository Index and Targeted Context](../../tools/context/README.md) documents the derived-state authority, versioned JSON index, commit and fingerprint freshness, immutable-per-run repository view, progressive selector, exclusions, restrictions, fallback, manifests, commands, and limitations.
- `python3 -m tools.context index` builds generated metadata-only repository evidence using one source read per metadata-bearing governed asset.
- `python3 -m tools.context select --story EFF-IDX-001` selects deterministic context and explains category, reason, relationship path, mandatory state, restriction, expansion level, completeness, and fallback.
- Focused standard-library tests cover determinism, identity conflicts, relationships, freshness, stability, exclusions, absence of source bodies, hierarchy, standards, targets, dependencies, restrictions, unresolved references, stale regeneration, expansion, and serialization.
- EFF-IDX-001 and EFF-SEL-001 are **In Review**. Sprint 5.2 is not complete until human review and Product Owner approval are recorded.

## Carried Finding

| Finding | Sprint 5.2 disposition |
| --- | --- |
| ARCH-REL004-006 | Materially addressed for indexing and context selection: one immutable repository view parses every metadata-bearing asset once per build and is reusable by later consumers. Existing validators were not broadly rewritten; validator integration and changed-file execution remain assigned to EFF-VAL-001 in Sprint 5.4. |
