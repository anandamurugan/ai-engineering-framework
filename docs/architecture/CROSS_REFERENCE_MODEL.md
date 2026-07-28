# Cross-Reference Model

## Purpose

The model defines how framework assets express durable, navigable, and machine-readable relationships. Stable identifiers describe identity; relative Markdown links provide repository navigation.

## Relationship types

| Relationship | Direction and meaning | Requirement | Future reference |
| --- | --- | --- | --- |
| `belongs_to` | Child → owning release, epic, sprint, or catalog | Required when the asset has a declared parent | Not permitted |
| `implements` | Implementing asset → requirement, decision, or design it realizes | Required when conformance is claimed | Not permitted |
| `governed_by` | Governed asset → policy or standard that constrains it | Required when a governing source applies | Not permitted |
| `related_to` | Source ↔ peer with meaningful non-authoritative affinity | Optional and symmetric | Permitted as planned text only |
| `depends_on` | Dependent asset → prerequisite required for valid use | Required when the source cannot operate independently | Not permitted |
| `supersedes` | New asset → older asset it replaces | Required for replacement | Not permitted |
| `validated_by` | Asset or rule → validation rule that evaluates it | Optional until a validator exists | Permitted as planned text only |
| `used_by` | Reusable asset → known consumer | Optional inverse navigation | Permitted as planned text only |
| `produces` | Process asset → output asset or evidence type | Required when output defines completion | Future type permitted as planned text |
| `consumes` | Process asset → required input asset or evidence type | Required for essential inputs | Not permitted |
| `requires_evidence_from` | Decision or requirement → source responsible for evidence | Required when another asset supplies approval evidence | Not permitted |

“Planned text only” means a prose statement naming the intended stable ID or type without a Markdown link or active metadata dependency. Planned references do not satisfy readiness, conformance, or approval.

## Direction and inverse relationships

Relationships are recorded from the asset whose behavior or meaning depends on the target. Inverse relationships MAY be shown for navigation but MUST NOT contradict the authoritative direction.

Examples:

- a story `belongs_to` a sprint;
- a standard is `used_by` a playbook;
- a playbook `implements` a standard;
- a newer standard `supersedes` an older standard.

Symmetric `related_to` relationships SHOULD appear in both assets when useful. Directed relationships do not become symmetric merely because both assets mention each other.

## YAML representation

Asset-specific schemas determine supported fields. Standard front matter uses specialized relationship arrays:

```yaml
supersedes:
  - STD-ARCH-000
related_standards:
  - STD-SEC-001
related_playbooks:
  - PB-FEAT-001
```

A future generalized relationship schema may use:

```yaml
relationships:
  - type: governed_by
    target: POL-SEC-001
  - type: requires_evidence_from
    target: VAL-META-001
```

The generalized form is illustrative and not an implemented schema.

## Markdown representation

Prose lists the stable ID and a relative link. Authors construct the link only after the target exists:

```text
Link label: <stable standard ID> — <standard title>
Link target: <relative path to the existing standard file>
```

Link labels SHOULD include the stable ID and title. Directory paths alone are not identities.

## Integrity rules

1. An active relationship target MUST exist and have the stated stable ID.
2. Repository links MUST be relative and resolve with exact filename case.
3. Metadata IDs and Markdown labels MUST agree.
4. A planned future target MUST NOT appear as an active metadata dependency or broken link.
5. Circular `belongs_to`, `depends_on`, `implements`, `supersedes`, and `requires_evidence_from` relationships are prohibited.
6. `related_to` cycles are permitted because they carry no dependency or authority.
7. An asset MUST NOT both supersede and depend on the same target.
8. Relationships MUST NOT imply approval, authority, or conformance beyond the target's status.
9. A lower-authority asset MUST NOT use relationships to override a governing source.
10. File moves MUST update links without changing stable IDs.

## Required examples

The following show valid relationship intent. Only links to existing assets are active.

### Release to Epic

[REL-004](../../product/releases/REL-v0.4.md) contains and is `used_by` [EPIC-001](../../product/epics/EPIC-001-enterprise-standards-framework.md); the epic `belongs_to` the release.

### Epic to Sprint

[EPIC-001](../../product/epics/EPIC-001-enterprise-standards-framework.md) contains [SPR-004-001B](../../product/sprints/SPR-004-001B-standards-foundation.md); the sprint `belongs_to` the epic.

### Sprint to Story

[SPR-004-001B](../../product/sprints/SPR-004-001B-standards-foundation.md) contains [STD-INF-006](../../product/stories/STD-INF-006-cross-reference-model.md); the story `belongs_to` the sprint.

### Story to Standard

A future Sprint 4.2 story may `produce` a standard. This is a planned relationship until both assets exist and must not be expressed as a broken link.

### Standard to Standard

A standard lists existing peers under `related_standards`; a replacement lists the prior standard under `supersedes`. Sprint 4.2 relationships remain planned until files exist.

### Standard to Playbook

A standard lists an existing consumer under `related_playbooks`; a playbook `implements` the standard. The current [feature development playbook](../../playbooks/feature-development.md) predates versioned standard IDs, so no ID relationship is asserted.

### Agent Profile to Standard

An agent profile is `governed_by` the standards that constrain its work. The current [orchestrator role](../../agents/orchestrator.md) predates versioned IDs; future migration must preserve this direction.

### Workflow to Playbook

The existing [analyze and plan workflow](../../workflows/01-analyze-plan.md) `implements` the [feature development playbook](../../playbooks/feature-development.md).

### Validation Rule to Standard

A future validation rule `implements` a deterministic check and is referenced by a standard through `validated_by`. No validation catalog or engine currently exists.

## Review

Authors validate link resolution, target identity, direction, lifecycle status, cycles, and authority during review. The [Standards Review Process](../governance/STANDARD_REVIEW_PROCESS.md) governs relationship approval.
