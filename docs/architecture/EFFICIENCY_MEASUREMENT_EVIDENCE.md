---
id: architecture.efficiency-measurement-evidence
title: Efficiency Measurement and Evidence Contract
version: 0.5.0
status: proposed
owner: Framework Maintainers
tags:
  - architecture
  - execution
  - measurement
  - evidence
ai_consumable: true
human_reviewed: false
last_updated: 2026-08-09
---

# Efficiency Measurement and Evidence Contract

## Purpose

This document is the authoritative EFF-MET-001 contract for vendor-neutral execution-efficiency measurement and evidence. It complements the [Execution Efficiency and Context Management contract](EXECUTION_EFFICIENCY_CONTEXT_MANAGEMENT.md) and defines comparable semantics without assuming that a platform exposes token counts, prices, or a particular execution runtime.

Metrics provide evidence for review and improvement. They do not approve an execution, establish quality by themselves, or authorize a governance decision.

## Measurement Principles

- Quality, security, privacy, correctness, validation, and governance outcomes take precedence over resource reduction.
- Every measure MUST define its unit, scope, collection boundary, source revision or execution identity, and unavailable-value behavior.
- An unavailable value MUST be reported as unavailable rather than zero.
- Measurements SHOULD distinguish initial context, expanded context, reused context, and evidence output.
- Counts MUST avoid combining dissimilar concepts under an unexplained total.
- Platform-specific telemetry MAY supplement the common contract but MUST NOT redefine normative semantics.
- Token consumption MAY be recorded when available but MUST NOT be the primary architecture or sole success measure.

## Execution Measurement Boundary

An efficiency record SHOULD identify:

- execution or checkpoint identifier;
- bounded objective and task type;
- repository or asset source revision;
- execution start and completion state;
- applicable execution profile;
- capability tier or deterministic-tool class;
- measurement availability and collection method; and
- known exclusions or limitations.

Metrics from materially different boundaries MUST NOT be compared without identifying the difference.

## Common Metrics

| Metric | Definition | Unit or representation | Unavailable behavior |
| --- | --- | --- | --- |
| Relevant-context ratio | Task-relevant context loaded divided by all loaded context, using a documented relevance assessment | Ratio with numerator and denominator | Report unavailable when relevance cannot be assessed reliably. |
| Files loaded | Distinct files whose content entered execution context | Count, optionally split by initial, expanded, and reused | Report unavailable when the platform cannot distinguish file access from content loading. |
| Context bytes loaded | Encoded or raw content bytes supplied as context, with encoding semantics stated | Bytes | Report unavailable; do not estimate silently. |
| Retrieved assets | Distinct governed or indexed assets retrieved for consideration | Count by asset type where practical | Report unavailable when asset identity is not observable. |
| Retrieval operations | Repository, index, or knowledge retrieval actions | Count by mechanism class | Report unavailable when operations are not observable. |
| Context expansions | Material additions beyond the initial context boundary | Count plus expansion reasons | Report unavailable only when the execution cannot observe expansion events. |
| Repeated repository scans | Materially equivalent scans over the same scope and source revision | Count with scope identity | Report unavailable when scan identity is not observable. |
| Execution invocations | Distinct deterministic, AI, or human-directed execution calls used for the task | Count by conceptual capability tier or tool class | Report unavailable rather than inferring from messages. |
| Tool invocations | Calls to repository, build, test, validation, deployment, or other tools | Count by tool class | Report unavailable when the environment provides no call evidence. |
| Retry count | Re-executions intended to obtain the same outcome after failure | Count with changed-input or method reason | Report unavailable when retries cannot be distinguished. |
| Equivalent failures | Repeated materially identical failures without meaningful state or method change | Count by failure signature | Report unavailable when failure signatures cannot be compared. |
| Execution duration | Elapsed time for the defined execution boundary | Duration with clock basis | Report unavailable when reliable timestamps do not exist. |
| Tier escalation | Transition to a stronger capability or accountable human tier | Count plus source tier, target tier, and reason | Report no escalation only when routing events are observable. |
| Checkpoint resume success | Resume attempts that reconstruct required state and continue correctly | Successful resumes divided by assessed resume attempts | Report unavailable when no resume assessment occurred. |
| Reusable-context utilization | Reused governed context divided by eligible stable context | Ratio with eligibility definition | Report unavailable when eligibility or reuse is not observable. |
| Validation scope ratio | Assets scanned by targeted validation compared with the defined full-validation population | Ratio with both counts and selection mode | Report unavailable when the full population is unknown. |
| Targeted-to-full validation | Number of targeted validation executions relative to full executions | Counts and ratio over a defined period or task set | Report unavailable when execution modes are not recorded. |
| Token usage | Platform-reported input, output, cached, or other token categories | Counts with platform semantics | Report unavailable on platforms without reliable token telemetry. |

## Relevant Context Assessment

Context is relevant when it materially supports an applicable requirement, target behavior, dependency, validation obligation, security or privacy assessment, decision, or evidence need for the bounded objective.

Relevance SHOULD be assessed using explicit relationships and observed use where practical. Context is not automatically irrelevant because it did not lead to a code change, and it is not automatically relevant because it was available or retrieved.

The relevant-context ratio MUST NOT be optimized independently. A high ratio paired with missed dependencies, failed validation, or insufficient evidence is a failed execution outcome.

## Expansion and Escalation Evidence

A material context-expansion record SHOULD include:

- prior context boundary;
- triggering fact or uncertainty;
- assets, relationship scope, or context class added;
- authorization and sensitive-data handling;
- budget effect;
- result and whether the expansion resolved the need.

A material capability-escalation record SHOULD include:

- initial and selected tiers;
- routing factors and observed limitation;
- retry or reassessment already performed;
- expected benefit and governance effect;
- outcome and any human decision required.

## Quality-Paired Measures

Efficiency evidence MUST be reviewed with applicable outcome measures, including:

- acceptance criteria satisfied;
- required validation executed and result;
- tests executed and result;
- defects or regressions introduced;
- affected dependencies identified;
- security and privacy controls satisfied;
- evidence completeness;
- required human reviews and approvals obtained; and
- unresolved findings, exceptions, or residual risks.

An execution that uses more context or a higher tier may be the correct and more efficient enterprise outcome when it prevents rework, avoids risk, or supplies necessary evidence.

## Anti-Gaming Controls

Metrics MUST NOT incentivize or reward:

- insufficient context or concealed dependency impact;
- skipped, narrowed, suppressed, or falsely reported validation;
- use of an inadequate capability for high-risk work;
- suppression or misclassification of retries and equivalent failures;
- omitted expansion, escalation, exception, or checkpoint evidence;
- avoided specialist or human escalation;
- reduced security, privacy, architecture, documentation, or domain review;
- reuse of stale or unauthorized context; or
- reporting unavailable telemetry as zero.

Efficiency evaluation MUST reject a favorable resource metric when paired quality or governance controls fail. Cost or resource reduction MUST NOT waive a mandatory control.

## Evidence Representation

Machine-readable evidence SHOULD support:

- stable field names and schema version;
- source revision and execution identity;
- explicit units and collection methods;
- values, unavailable state, and limitations;
- initial, expanded, reused, and excluded context categories;
- routing, retry, loop, checkpoint, and validation events;
- paired quality and governance outcomes; and
- provenance sufficient to distinguish measured values, derived values, assertions, and human decisions.

The evidence format MUST NOT embed credentials, secrets, unnecessary personal data, or unrestricted sensitive context. Evidence retention and access follow applicable policy.

The v0.5 derived context and execution artifacts use a small common provenance envelope containing evidence format/type, repository revision, applicable index fingerprint, execution/task identity, UTC timestamp, runtime, operation, requested/effective scope, source asset, authority, and result where available. Optional unavailable fields are omitted rather than invented. Validation report format 2.0 retains its established field names and adds compatible common fields without changing result or count semantics. Every shared envelope marks derived execution evidence as not approval.

## Baselines and Comparisons

Projects MAY establish baselines by task class, risk level, repository scale, execution profile, or capability tier. Comparisons MUST disclose material differences in scope, quality gates, telemetry availability, and source state.

This contract does not set universal improvement percentages or target values. Later projects may set governed objectives only when they preserve quality and risk controls.

## Future Sprint Conformance

### Sprint 5.2

Repository indexing and context selection MUST expose source revision, assets considered, assets selected, exclusions, expansions, retrieval operations, freshness, and fallback. Measurements MUST distinguish index lookup from source-content loading.

### Sprint 5.3

Budgets, checkpoints, loops, and routing MUST expose configured dimensions, consumption, exhaustion response, checkpoint/resume outcome, equivalent failures, tiers, escalation reasons, and human-decision handoff.

### Sprint 5.4

Targeted validation MUST expose requested scope, affected closure, actual files or assets scanned, full-population basis, fallback reason, validator set, errors, warnings, incomplete execution, and evidence provenance.

The v0.5 context, execution-governance, and validation packages implement these conformance interfaces where measurements are locally observable. External execution telemetry and cross-run aggregation remain outside v0.5.

## Human Authority

Metrics and automated evidence MAY inform routing, planning, validation, and review. They MUST NOT accept risk, approve exceptions, waive standards, suppress validation, approve architecture or security, authorize deployment, authorize release, or infer Product Owner approval.
