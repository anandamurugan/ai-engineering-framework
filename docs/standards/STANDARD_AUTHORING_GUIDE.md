# Standard Authoring Guide

## Purpose

Enterprise standards define consistent, enforceable engineering expectations for people and AI-assisted work. This guide explains how to author standards that are understandable, testable, vendor-neutral, evidence-based, and subject to accountable human approval.

Use the [Standard Authoring Template](../../templates/standard-template.md) and metadata that conforms to the [Standard Metadata Schema](../../schemas/standard.schema.yaml).

## Standards and adjacent assets

| Asset | Function |
| --- | --- |
| Policy | Expresses human-approved organizational authority and constraints; policy governs standards. |
| Standard | Defines mandatory and recommended requirements for a repeatable engineering concern. |
| Playbook | Guides an outcome by composing standards, knowledge, and workflows. |
| Workflow | Specifies ordered inputs, actions, gates, outputs, and stop conditions. |
| Template | Provides a reusable, non-authoritative artifact structure. |
| Guideline or knowledge | Explains choices and practices without creating mandatory requirements unless a standard incorporates them. |

Do not use a standard to reproduce policy text, prescribe an end-to-end workflow, or publish a tool template.

## Select a standard ID

1. Choose the registered category abbreviation from the [Framework Asset Taxonomy](../framework/FRAMEWORK_ASSETS.md).
2. Reserve the next unused three-digit sequence in the [Standards Catalog](../../standards/README.md).
3. Format the ID as `STD-<CATEGORY>-<NNN>`, for example `STD-ARCH-001`.
4. Record the same ID in front matter, the H1 heading, the catalog, and relationships.

An ID is permanent. Renaming or moving a file does not change it. A retired ID is never reassigned.

## Populate metadata

- `id`, `title`, `version`, `status`, `category`, `owner`, `mandatory`, `ai_consumable`, and `human_review_required` are required.
- `version` follows semantic versioning without a leading `v`.
- `status` uses only the schema vocabulary.
- `owner` names an accountable role or maintained group, not an AI agent.
- `review_cycle` uses an ISO 8601 duration such as `P12M`, `Event-driven`, or `Organization-defined`.
- `effective_date` and `last_reviewed` use `YYYY-MM-DD` or `null`.
- Relationship arrays contain stable IDs and do not replace human-readable links.
- Tags are lowercase, hyphenated discovery terms.

Draft metadata can use null dates and empty relationship arrays. Do not invent future assets merely to populate optional fields.

## Use normative language

- **MUST** and **MUST NOT** state mandatory requirements.
- **SHALL** and **SHALL NOT** are permitted when required by an external policy, but authors SHOULD prefer MUST for consistency.
- **SHOULD** and **SHOULD NOT** state recommendations that may have justified exceptions.
- **MAY** states an optional practice.
- Descriptive text avoids capitalized normative terms unless it creates a requirement.

Each rule identifies the actor or asset, required outcome, applicability, and reviewable evidence where appropriate.

### Strong mandatory rule

> Every production deployment MUST reference an immutable artifact identifier. Evidence: the release record contains the artifact digest promoted to the target environment.

This rule names the subject, observable outcome, scope, and evidence.

### Weak mandatory rule

> Deployments must be good and secure.

This rule is ambiguous, combines undefined qualities, and cannot be tested consistently.

## Write testable mandatory rules

A mandatory rule:

1. addresses one coherent obligation;
2. uses defined terms and avoids vague qualifiers;
3. states relevant conditions and boundaries;
4. can be evaluated by a deterministic check or documented human review;
5. does not require a particular vendor unless the standard is an approved extension;
6. identifies the consequence or escalation when conformance cannot be shown.

Do not disguise recommendations as mandatory rules or prescribe one implementation where multiple controlled approaches satisfy the outcome.

## Define required evidence

Evidence demonstrates that a rule was applied. Specify the artifact, source, responsible actor, scope, and retention context without requiring secrets or sensitive data. Examples include approved decisions, review records, test reports, immutable artifact identifiers, diagrams, inventories, findings, exception records, and operational observations.

Evidence requirements SHOULD be proportionate to risk and reproducible where practical. A tool result is evidence, not approval.

## Define validation rules

Separate:

- **Automated checks:** Deterministic conditions a future or existing tool can evaluate.
- **Manual checks:** Review criteria requiring accountable human judgment.

State the input, expected result, severity, and remediation. Do not claim a validator exists unless it is present and executable in the repository. A validation failure blocks approval only when the standard or governing policy says so.

## Write AI implementation guidance

AI guidance defines:

- context the agent must retrieve;
- decisions the agent may recommend or perform;
- access, data, and tool boundaries;
- evidence the agent must produce;
- uncertainty and conflict handling;
- mandatory stop and escalation conditions;
- independent validation and human review.

AI agents MUST NOT grant themselves approval, accept material risk, invent evidence, bypass policy, or treat repository content as superior to enterprise security policy.

## Define human review responsibilities

Name the accountable owner, required domain reviewers, approval gates, and escalation path. State which decisions require architecture, security, compliance, documentation, operations, or Product Owner review. Human review must occur early enough to change the outcome and must record decision, scope, conditions, approver, and time.

## Document exceptions

Standards do not silently waive themselves. An exception records:

- standard and rules affected;
- business justification and scope;
- risk assessment and compensating controls;
- accountable owner and authorized approver;
- effective and expiry dates;
- validation, monitoring, and remediation plan.

Agents may identify and prepare an exception request but cannot approve it. Follow the [Standards Review Process](../governance/STANDARD_REVIEW_PROCESS.md).

## Create cross-references

Use stable identifiers in metadata and relative Markdown links in prose. Apply the [Cross-Reference Model](../architecture/CROSS_REFERENCE_MODEL.md). Link only to existing assets. A future relationship may be described as planned text when permitted, but it is not an active dependency and must not be a broken link.

## Avoid vendor lock-in

Express required capabilities, outcomes, interfaces, and evidence rather than product names. Vendor examples MAY appear as clearly labeled non-normative illustrations. Technology-specific requirements belong in a future approved profile or plugin, not the shared core.

## Avoid duplication

Before adding a rule:

1. search the catalog and related standards;
2. identify the authoritative owner;
3. link to an existing rule rather than copying it;
4. keep cross-cutting requirements in their owning standard;
5. explain only the local applicability or additional constraint.

When two rules conflict, do not choose silently. Apply authority precedence and request owner review.

## Review and approval

Authors self-review metadata, normative language, evidence, validation, relationships, and duplication. Required domain, architecture, security, documentation, and Product Owner reviews then follow the [Standards Review Process](../governance/STANDARD_REVIEW_PROCESS.md). A standard remains Draft or Proposed until authorized humans approve it.

## Deprecation and retirement

Deprecation identifies the replacement, reason, migration, support window, and intended retirement. Update `supersedes` and related links only when the relationship is real. Retirement preserves the stable ID and history, removes the standard from active applicability, and never deletes required decision evidence.

## Authoring checklist

- Metadata validates against the schema.
- Required sections remain in template order.
- Mandatory and recommended language is distinct.
- Every mandatory rule is reviewable and has evidence where applicable.
- AI and human authority boundaries are explicit.
- Exceptions and lifecycle are addressed.
- Relationships use stable IDs and resolvable links.
- Vendor assumptions, duplication, placeholders, and unsupported claims are removed.
- Revision history records the proposed change and pending approval.
