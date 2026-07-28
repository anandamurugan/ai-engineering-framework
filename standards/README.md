# Standards Catalog

## Purpose

The `standards/` directory contains mandatory and recommended engineering controls for the Enterprise AI SDLC Framework. The catalog is the authoritative navigation and status index; it does not confer approval by itself.

## Organization

Approved v0.4 standards will be organized by category under `standards/<category>/` and authored with:

- [Framework Asset Taxonomy](../docs/framework/FRAMEWORK_ASSETS.md)
- [Standard Metadata Schema](../schemas/standard.schema.yaml)
- [Standard Authoring Template](../templates/standard-template.md)
- [Standard Authoring Guide](../docs/standards/STANDARD_AUTHORING_GUIDE.md)
- [Cross-Reference Model](../docs/architecture/CROSS_REFERENCE_MODEL.md)
- [Standards Review Process](../docs/governance/STANDARD_REVIEW_PROCESS.md)
- [Documentation Style Guide](../docs/contributing/DOCUMENTATION_STYLE_GUIDE.md)

## Status definitions

| Status | Meaning |
| --- | --- |
| Draft | Work in progress; not approved for application. |
| Proposed | Submitted for required reviews; not yet approved. |
| Approved | Approved by the Product Owner after required specialist reviews. |
| Deprecated | Still discoverable but scheduled for replacement or retirement. |
| Retired | No longer active; retained for history and traceability. |

## Category definitions

Categories group standards by durable engineering concern, such as Architecture, Coding, API, Testing, Documentation, Git, Pull Request, Dependency Management, Security, Delivery, Operations, and Governance. New categories require catalog review and must not duplicate an existing concern.

## Versioned standards

No v0.4 standard is approved yet.

| ID | Title | Category | Version | Status | Owner | Mandatory | Link |
| --- | --- | --- | --- | --- | --- | --- | --- |
| — | No versioned standards published | — | — | — | — | — | — |

## Existing foundational controls

The repository contains pre-v0.4 controls that remain applicable but have not yet been migrated to the v0.4 standard schema. Migration requires separate review; this foundation task does not assign IDs or approval metadata retroactively.

| Document | Status | Link |
| --- | --- | --- |
| Definition of Ready | Existing control | [Read](definition-of-ready.md) |
| Definition of Done | Existing control | [Read](definition-of-done.md) |
| Human-in-the-Loop Standard | Existing control | [Read](human-in-the-loop.md) |
| Risk Classification Standard | Existing control | [Read](risk-classification.md) |

## Planned standards

Sprint 4.2 plans Architecture, Coding, API Design, Testing, Documentation, Git and Branching, Pull Request, and Dependency Management standards. These assets are not implemented or approved, have no active catalog links, and must not be treated as requirements.

## Catalog maintenance

Authors add a standard only when its file exists and metadata is internally consistent. IDs are unique and stable. Status changes follow the review process. Deprecated and retired entries remain visible with replacement information where applicable.
