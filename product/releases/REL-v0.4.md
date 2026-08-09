---
id: REL-004
title: Release v0.4 - Enterprise Standards Framework
version: 0.4.0
status: Released
owner: Framework PMO
target_release: 2026-08-08
---

# Release v0.4 – Enterprise Standards Framework

## Objective

Establish the Enterprise Standards Framework that defines how AI agents and human engineers design, develop, review, validate, and deliver software consistently across the Software Development Life Cycle.

## Scope

This release introduces the foundational standards that govern engineering practices for the Enterprise AI SDLC Framework.

### Included

- Standards Foundation
- Architecture Standards
- Coding Standards
- API Standards
- Testing Standards
- Security Standards
- Documentation Standards
- DevOps Standards
- Observability Standards
- Performance Standards
- Governance Standards
- Governance validation and CI conformance evidence

### Excluded

- SDLC Playbooks planned for v0.5
- Agent Catalog planned for v0.6
- Workflow Library planned for v0.7
- Prompt and Tool Adapter Framework planned for v0.8

## Success Criteria

- Standard metadata schema approved.
- Standard authoring template published.
- Standards catalog completed.
- Core engineering standards documented.
- Governance process established.
- Cross-reference model implemented.
- Internal documentation links validated.

## Deliverables

| ID | Deliverable |
| --- | --- |
| EPIC-001 | Enterprise Standards Framework |
| SPR-004-001B | Standards Foundation |
| SPR-004-002 | Core Engineering Standards |
| SPR-004-003 | Enterprise Engineering Standards |
| SPR-004-004 | Governance and Validation |

Sprint 4.1B through Sprint 4.4 are complete. Architecture Review conditions are satisfied, Domain Review is Approved, Documentation Review conditions are satisfied, Security Review is Approved with Accepted Residual Risk, and Product Owner approval is recorded. This release record is prepared for the final main release commit; the `v0.4.0` tag remains pending until that commit is merged and validated.

## Risks

| Risk | Response |
| --- | --- |
| Inconsistent documentation | Enforce a common authoring template and style guide. |
| Missing traceability | Require stable asset identifiers and cross-references. |
| Unclear ownership | Require ownership metadata for every standard. |
| Scope expansion | Keep validation bounded to approved Sprint 4.4 conformance checks and defer playbooks, agents, prompts, vendor integrations, and unrelated tooling. |
| Weak AI usability | Include explicit AI guidance and machine-readable metadata. |

## Exit Criteria

- All v0.4 sprint deliverables are completed.
- Required standards are published.
- Metadata and cross-references are validated.
- Architecture review is approved.
- Domain review is approved.
- Documentation review is approved.
- Security review is approved or its residual risks are explicitly accepted by an authorized human.
- Product Owner approves the release.
- Release is tagged as `v0.4.0`.

## Release Readiness Checklist

| Gate | Status | Evidence or required action |
| --- | --- | --- |
| All REL-004 planned sprint implementations complete | Complete | SPR-004-001B through SPR-004-004 deliverables exist; lifecycle approval remains separate. |
| Standards catalog complete | Complete | Catalog parity validator reports no mismatches. |
| Standards lifecycle status correct | Complete | All 15 versioned standards remain Draft because release-wide review evidence does not satisfy the standard-specific approval-record requirements. |
| Full validation | Complete | Twelve registered validators report PASS with no errors. |
| Test suite | Complete | Standard-library validation tests pass. |
| Hosted CI | Complete | `Framework Validation / Framework validation` passes on the default branch. |
| Changelog | Complete | The v0.4.0 entry is finalized with the release date and deferred items. |
| README and roadmap accuracy | Complete | v0.4.0 is represented as released without presenting deferred capabilities as implemented. |
| Architecture review | Approved with Conditions — Satisfied | ARCH-REL004-001 documentation remediation and validation evidence are recorded in [SPR-004-004](../sprints/SPR-004-004-governance-validation.md#architecture-review-evidence). |
| Domain review | Approved | The human Domain Review decision is Approved; six non-blocking findings remain tracked for future follow-up. No reviewer identity, signature, or timestamp is inferred. |
| Documentation review | Approved with Conditions — Satisfied | DOC-REL004-001 through DOC-REL004-006 were remediated and repository validation passed. No reviewer identity, signature, or timestamp is inferred. |
| Security specialist review | Approved with Accepted Residual Risk | The authorized human decision accepts SEC-REL004-001 and SEC-REL004-002 for v0.4.0 and retains SEC-REL004-003 through SEC-REL004-006 as non-blocking follow-up. No reviewer identity, signature, credentials, or timestamp is inferred. |
| Product Owner approval | Complete | Product Owner explicitly approved REL-004 / v0.4.0 for release; this decision does not satisfy other required reviews. |
| Known gaps accepted or deferred | Complete | Product Owner dispositions are recorded below; advisory findings remain visible. |
| Release version and target confirmed | Complete | Version is `0.4.0`; release date is `2026-08-08`, the date of this controlled release closeout. |
| Release tag | Pending | Create `v0.4.0` only after all release gates are approved. |

## Release Record

- Version: **v0.4.0**
- Release date: **2026-08-08**
- Release status: **Released when this release commit is merged to `main` and final hosted validation passes**
- Tag status: **Pending**; the tag must identify the final validated `main` commit.

## Product Owner Decision

Product Owner Approval: **Approved**

Scope: REL-004 / v0.4.0.

No reviewer identity, signature, timestamp, or approval for another role is inferred from this decision.

### Residual Gap Dispositions

| Gap | Product Owner disposition | Current evidence |
| --- | --- | --- |
| Dedicated Markdown linter | Deferred to future backlog; deterministic Markdown hygiene is accepted for v0.4. | `VAL-HYGIENE-MARKDOWN-001` remains the implemented coverage. |
| Repository-owned secret scanner | Deferred to future backlog; absence remains documented and is not represented as implemented. | The external local commit hook is supplemental and not repository CI enforcement. |
| Branch protection | Repository administration action. | Enable or verify the required status check `Framework Validation / Framework validation`; current protection status is unverified. |
| Five non-reciprocal `related_standards` findings | Accepted for v0.4 while the validator classifies them as optional advisory warnings. | Findings remain visible as WARNING results and are not suppressed. |

These Product Owner dispositions did not substitute for Security Review. The separate authorized Security Review decision and its accepted residual risks are recorded below; final hosted validation of the merged release commit and tagging remain separate controls.

## Security Review Decision

Security Review: **APPROVED WITH ACCEPTED RESIDUAL RISK**

No reviewer identity, signature, credentials, or timestamp is inferred from the supplied human decision.

| Finding | Release disposition | Required follow-up |
| --- | --- | --- |
| SEC-REL004-001 | Accepted as a temporary repository-administration risk for v0.4.0. Branch protection and required status-check enforcement remain unverified; acceptance is conditional on Framework Validation passing on the final `main` release commit. | Verify or configure branch protection requiring `Framework Validation / Framework validation`. |
| SEC-REL004-002 | Accepted for v0.4.0 given the documentation-oriented framework, dependency-free validation tooling, absence of CI-required repository secrets, and completed targeted inspection. Repository-owned secret scanning remains absent. | Implement governed repository-owned secret scanning in a future release. |
| SEC-REL004-003 | Non-blocking follow-up. | Add a governed repository `SECURITY.md` without inventing disclosure contacts. |
| SEC-REL004-004 | Non-blocking follow-up. | Evaluate checkout credential hardening and governed ownership or CODEOWNERS controls. |
| SEC-REL004-005 | Non-blocking follow-up. | Improve validation-evidence provenance and integrity. |
| SEC-REL004-006 | Non-blocking follow-up. | Add validator resource-bound robustness as scale or exposure warrants. |

Accepted risk is a release disposition, not remediation. The underlying gaps remain visible and do not become implemented capabilities through approval.
