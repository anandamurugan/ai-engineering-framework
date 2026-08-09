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

The following standards were delivered by v0.4.0 and remain Draft. Release-wide reviews and Product Owner approval do not replace the standard-specific approval record required by the [Standards Review Process](../docs/governance/STANDARD_REVIEW_PROCESS.md), including the standard ID and version, reviewers, decision, date, evidence, and residual risk.

| ID | Title | Category | Version | Status | Owner | Mandatory | Link |
| --- | --- | --- | --- | --- | --- | --- | --- |
| STD-ARCH-001 | Architecture Standard | Architecture | 0.4.0 | Draft | Framework PMO | Yes | [Read](architecture/STD-ARCH-001-architecture-standard.md) |
| STD-CODE-001 | Coding Standard | Coding | 0.4.0 | Draft | Framework PMO | Yes | [Read](coding/STD-CODE-001-coding-standard.md) |
| STD-API-001 | API Design Standard | API | 0.4.0 | Draft | Framework PMO | Yes | [Read](api/STD-API-001-api-design-standard.md) |
| STD-TEST-001 | Testing Standard | Testing | 0.4.0 | Draft | Framework PMO | Yes | [Read](testing/STD-TEST-001-testing-standard.md) |
| STD-DOC-001 | Documentation Standard | Documentation | 0.4.0 | Draft | Framework PMO | Yes | [Read](documentation/STD-DOC-001-documentation-standard.md) |
| STD-GIT-001 | Git and Branching Standard | Git | 0.4.0 | Draft | Framework PMO | Yes | [Read](git/STD-GIT-001-git-and-branching-standard.md) |
| STD-PR-001 | Pull Request Standard | Pull Request | 0.4.0 | Draft | Framework PMO | Yes | [Read](pull-request/STD-PR-001-pull-request-standard.md) |
| STD-DEP-001 | Dependency Management Standard | Dependency Management | 0.4.0 | Draft | Framework PMO | Yes | [Read](dependency-management/STD-DEP-001-dependency-management-standard.md) |
| STD-SEC-001 | Enterprise Security Standard | Security | 0.4.0 | Draft | Framework PMO | Yes | [Read](security/STD-SEC-001-enterprise-security-standard.md) |
| STD-PERF-001 | Performance and Scalability Standard | Performance | 0.4.0 | Draft | Framework PMO | Yes | [Read](performance/STD-PERF-001-performance-scalability-standard.md) |
| STD-OBS-001 | Observability Standard | Observability | 0.4.0 | Draft | Framework PMO | Yes | [Read](observability/STD-OBS-001-observability-standard.md) |
| STD-DEPLOY-001 | Deployment Standard | Deployment | 0.4.0 | Draft | Framework PMO | Yes | [Read](deployment/STD-DEPLOY-001-deployment-standard.md) |
| STD-REL-001 | Release Management Standard | Release Management | 0.4.0 | Draft | Framework PMO | Yes | [Read](release/STD-REL-001-release-management-standard.md) |
| STD-INC-001 | Incident Management Standard | Incident Management | 0.4.0 | Draft | Framework PMO | Yes | [Read](incident/STD-INC-001-incident-management-standard.md) |
| STD-RISK-001 | Enterprise Risk Management Standard | Risk Management | 0.4.0 | Draft | Framework PMO | Yes | [Read](risk/STD-RISK-001-enterprise-risk-management-standard.md) |

## Existing foundational controls

The repository contains pre-v0.4 controls that remain applicable but have not yet been migrated to the v0.4 standard schema. Migration requires separate review; this foundation task does not assign IDs or approval metadata retroactively.

| Document | Status | Link |
| --- | --- | --- |
| Definition of Ready | Existing control | [Read](definition-of-ready.md) |
| Definition of Done | Existing control | [Read](definition-of-done.md) |
| Human-in-the-Loop Standard | Existing control | [Read](human-in-the-loop.md) |
| Risk Classification Standard | Existing control | [Read](risk-classification.md) |

## Governance and validation status

Sprint 4.4 implements executable framework validation, JSON conformance evidence, and GitHub Actions CI integration as documented in the [validation framework](../tools/validation/README.md). REL-004 / v0.4.0 release review is complete; the catalog does not confer approval on its Draft standards. Future v0.5 capabilities remain outside this catalog and are not represented as implemented requirements.

## Catalog maintenance

Authors add a standard only when its file exists and metadata is internally consistent. IDs are unique and stable. Status changes follow the review process. Deprecated and retired entries remain visible with replacement information where applicable.
