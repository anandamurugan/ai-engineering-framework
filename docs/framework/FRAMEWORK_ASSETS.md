# Framework Asset Taxonomy

## Purpose

The taxonomy defines the durable asset types used by the Enterprise AI SDLC Framework. It gives people and future tooling a shared vocabulary for identity, ownership, lifecycle, storage, and relationships.

## Stable identifiers

Every governed asset MUST have a globally unique identifier within the framework. The identifier:

- MUST remain stable when a title, filename, or directory changes;
- MUST NOT be reused after an asset is retired;
- MUST be recorded in the asset's authoritative metadata or heading;
- SHOULD be referenced together with a relative Markdown link;
- MUST follow the registered prefix and pattern for its asset type.

Identifiers use uppercase ASCII letters, digits, and hyphens. Sequence numbers are zero-padded to at least three digits. Release context MAY be embedded where the registered pattern specifies it.

Examples:

```text
REL-004
EPIC-001
SPR-004-001
STD-ARCH-001
STD-CODE-001
PB-FEAT-001
WF-FEATURE-001
AG-ARCH-001
PRM-REVIEW-001
TMP-STD-001
VAL-META-001
ADR-0006
POL-SEC-001
```

`SPR-004-001B` is permitted for a corrective or continuation sprint when a previously published identifier cannot be reassigned. New sprint plans SHOULD use numeric identifiers.

## Common metadata

All governed assets require, at minimum, a stable `id`, `title`, `version` or revision, `status`, and `owner`. Assets SHOULD also declare relationships, review state, applicable release, tags, and update date when their schema supports those fields.

Metadata is authoritative for machine processing. The Markdown title and prose are authoritative for human explanation. A mismatch MUST be resolved before approval.

## Asset types

| Asset type | Purpose | Prefix and example | Typical owner | Expected location |
| --- | --- | --- | --- | --- |
| Release | Define a versioned product outcome, scope, risks, and exit criteria | `REL-` — `REL-004` | Framework PMO | `product/releases/` |
| Epic | Group related outcomes and measurable value within a release | `EPIC-` — `EPIC-001` | Product Owner or Framework PMO | `product/epics/` |
| Sprint | Bound an increment, objective, stories, and acceptance criteria | `SPR-` — `SPR-004-001` | Framework PMO | `product/sprints/` |
| Story | Define an independently reviewable product requirement and deliverable | Registered domain prefix — `STD-INF-001` | Product Owner or delegate | `product/stories/` |
| Standard | State mandatory and recommended engineering requirements | `STD-<CATEGORY>-` — `STD-ARCH-001` | Named standard owner | `standards/<category>/` |
| Playbook | Guide an end-to-end outcome by composing standards and workflows | `PB-` — `PB-FEAT-001` | Practice owner | `playbooks/` |
| Workflow | Define ordered inputs, actions, gates, outputs, and stop conditions | `WF-` — `WF-FEATURE-001` | Process owner | `workflows/` |
| Agent Profile | Bound an agent role's mission, authority, evidence, and prohibitions | `AG-` — `AG-ARCH-001` | Agent governance owner | `agents/` |
| Prompt | Provide a reviewed task instruction for a bounded context | `PRM-` — `PRM-REVIEW-001` | Prompt owner | Future prompt catalog |
| Template | Provide a reusable, non-authoritative artifact structure | `TMP-` — `TMP-STD-001` | Artifact owner | `templates/` |
| Validation Rule | Define a deterministic conformance check and result | `VAL-` — `VAL-META-001` | Validation owner | Future validation catalog |
| Architecture Decision Record | Preserve an architectural decision, alternatives, and consequences | `ADR-` — `ADR-0006` | Architecture owner | `docs/adr/` |
| Policy | Express human-approved organizational authority and constraints | `POL-` — `POL-SEC-001` | Designated policy owner | Organization-defined policy location |
| Reference Architecture | Describe an approved reusable architecture pattern and constraints | `RA-` — `RA-PLATFORM-001` | Enterprise Architecture | `reference/architectures/` when introduced |
| Example or Reference Implementation | Demonstrate non-normative application of framework assets | `EX-` — `EX-API-001` | Example maintainer | `examples/` when introduced |

Locations marked future do not imply that a catalog, runtime, or implementation currently exists.

## Type contracts

### Release

- **Required metadata:** ID, title, version, status, owner, target release.
- **Lifecycle:** Planned → In Progress → Approved → Released → Superseded or Retired.
- **Relationships:** Contains epics and sprints; governed by release policy; produces release evidence.
- **Representation:** Markdown product record with scope, deliverables, risks, and exit criteria.
- **Machine considerations:** Dates, versions, status, and child identifiers use consistent scalar values.

### Epic

- **Required metadata:** ID, title, version, status, owner, release, priority.
- **Lifecycle:** Planned → In Progress → Approved or Completed → Retired.
- **Relationships:** Belongs to a release; contains sprints and stories; depends on approved decisions.
- **Representation:** Markdown product record with value, objectives, scope, metrics, and completion criteria.
- **Machine considerations:** Release and child relationships use stable IDs.

### Sprint

- **Required metadata:** ID, title, version, status, owner, release, epic.
- **Lifecycle:** Planned → In Progress → In Review → Approved or Completed.
- **Relationships:** Belongs to a release and epic; contains stories; produces review evidence.
- **Representation:** Markdown specification with objective, scope, stories, dependencies, and acceptance criteria.
- **Machine considerations:** Story lists SHOULD provide both stable IDs and resolvable links.

### Story

- **Required metadata:** ID, title, version, status, owner, release, epic, sprint, priority.
- **Lifecycle:** Proposed → Ready → In Progress → In Review → Approved or Done.
- **Relationships:** Belongs to a sprint, epic, and release; produces a named deliverable.
- **Representation:** Markdown requirement with value, scope, requirements, acceptance, validation, and approval.
- **Machine considerations:** The deliverable path and parent IDs SHOULD be explicit.

### Standard

- **Required metadata:** Defined by the [Standard Metadata Schema](../../schemas/standard.schema.yaml).
- **Lifecycle:** Draft → Proposed → Approved → Deprecated → Retired.
- **Relationships:** Governed by policy; related to standards; used by playbooks, workflows, and agent profiles; validated by rules.
- **Representation:** Markdown using the [Standard Authoring Template](../../templates/standard-template.md).
- **Machine considerations:** Front matter MUST validate against the schema; normative sections remain human-readable.

### Playbook

- **Required metadata:** ID, title, version, status, owner, applicable standards.
- **Lifecycle:** Draft → Proposed → Approved → Deprecated → Retired.
- **Relationships:** Implements standards; uses workflows; may consume templates and knowledge.
- **Representation:** Outcome-oriented Markdown guidance.
- **Machine considerations:** Ordered phases and required standards SHOULD be explicitly identifiable.

### Workflow

- **Required metadata:** ID, title, version, status, owner, inputs, outputs, gates.
- **Lifecycle:** Draft → Proposed → Approved → Deprecated → Retired.
- **Relationships:** Implements a playbook; consumes context; produces evidence; is governed by standards.
- **Representation:** Procedural Markdown with ordered steps and stop conditions.
- **Machine considerations:** Inputs, outputs, decisions, and gates SHOULD use stable names.

### Agent Profile

- **Required metadata:** ID, title, version, status, owner, authority boundary.
- **Lifecycle:** Draft → Proposed → Approved → Suspended, Deprecated, or Retired.
- **Relationships:** Governed by standards and policy; participates in workflows; produces evidence.
- **Representation:** Markdown role contract.
- **Machine considerations:** Permissions and prohibited actions MUST be distinguishable; approval authority MUST remain human.

### Prompt

- **Required metadata:** ID, title, version, status, owner, intended role, input and output constraints.
- **Lifecycle:** Draft → Evaluated → Approved → Deprecated → Retired.
- **Relationships:** Used by an agent profile; governed by standards; validated by evaluation evidence.
- **Representation:** Reviewed text with context, boundaries, and expected output.
- **Machine considerations:** Prompt content MUST NOT contain secrets; version and evaluation status MUST be retained.

### Template

- **Required metadata:** ID, title, version, status, owner, target asset type.
- **Lifecycle:** Draft → Proposed → Approved → Deprecated → Retired.
- **Relationships:** Used by authors; implements a schema or style guide.
- **Representation:** Markdown or another declared text format with authoring comments.
- **Machine considerations:** Placeholders MUST be distinguishable from production values.

### Validation Rule

- **Required metadata:** ID, title, version, status, owner, target contract, severity.
- **Lifecycle:** Draft → Tested → Approved → Deprecated → Retired.
- **Relationships:** Validates an asset or standard; produces a finding and evidence.
- **Representation:** Future machine-readable rule plus human explanation.
- **Machine considerations:** Inputs, deterministic result, severity, and remediation MUST be defined. No validation engine exists yet.

### Architecture Decision Record

- **Required metadata:** ID, title, version, status, owner, update date.
- **Lifecycle:** Proposed → Accepted or Rejected → Superseded or Deprecated.
- **Relationships:** Governs architecture; may supersede another ADR; is implemented by standards or designs.
- **Representation:** Markdown context, decision, alternatives, consequences, and implications.
- **Machine considerations:** Status and supersession links MUST be explicit.

### Policy

- **Required metadata:** ID, title, version, status, accountable owner, effective date.
- **Lifecycle:** Draft → Reviewed → Approved → Effective → Superseded or Retired.
- **Relationships:** Governs all lower-authority assets in scope; may require evidence or approval gates.
- **Representation:** Organization-approved policy in its authoritative system.
- **Machine considerations:** Scope, authority, effective date, and exceptions MUST be explicit.

### Reference Architecture

- **Required metadata:** ID, title, version, status, owner, applicability.
- **Lifecycle:** Draft → Architecture Review → Approved → Deprecated → Retired.
- **Relationships:** Implements ADRs and standards; used by solutions and examples.
- **Representation:** Markdown plus accessible diagrams and constraints.
- **Machine considerations:** Required and variable elements SHOULD be distinguishable.

### Example or Reference Implementation

- **Required metadata:** ID, title, version, status, owner, demonstrated assets.
- **Lifecycle:** Draft → Reviewed → Published → Deprecated → Retired.
- **Relationships:** Demonstrates standards, playbooks, workflows, or reference architectures.
- **Representation:** Clearly labeled non-normative content and, when later approved, implementation files.
- **Machine considerations:** Examples MUST NOT be interpreted as policy and SHOULD declare compatibility.

## Governance

New asset types or prefixes require Product Owner and appropriate architecture approval. Conflicts, aliases, and migrations follow the [Cross-Reference Model](../architecture/CROSS_REFERENCE_MODEL.md) and must preserve stable IDs.
