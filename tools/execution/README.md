# Execution Budgets, Checkpoints, and Routing

## Purpose

`tools.execution` implements EFF-BUD-001 and EFF-ROUTE-001 as deterministic, vendor-neutral execution governance. It evaluates supplied measurements and structured factors, persists derived state, detects equivalent failures, and recommends a conceptual capability tier. It never invokes a model, selects a named provider, authorizes restricted context, or makes a human governance decision.

The governing requirements are the [Execution Efficiency and Context Management contract](../../docs/architecture/EXECUTION_EFFICIENCY_CONTEXT_MANAGEMENT.md) and [Efficiency Measurement and Evidence Contract](../../docs/architecture/EFFICIENCY_MEASUREMENT_EVIDENCE.md). Repository and governance artifacts remain authoritative.

## Local Commands

Show available commands:

```shell
python3 -m tools.execution --help
```

Evaluate a measured state against a caller-supplied profile:

```shell
python3 -m tools.execution budget \
  --profile path/to/budget-profile.json \
  --state path/to/measured-state.json \
  --context-manifest .context-reports/context-manifest.json \
  --execution-id EXEC-001
```

Create and inspect a checkpoint:

```shell
python3 -m tools.execution checkpoint create \
  --input path/to/checkpoint-input.json

python3 -m tools.execution checkpoint inspect \
  --checkpoint .execution-reports/checkpoint.json
```

Evaluate failure repetition:

```shell
python3 -m tools.execution loop \
  --events path/to/failure-events.json \
  --threshold 3 \
  --response REASSESS \
  --execution-id EXEC-001 \
  --task-id STORY-001 \
  --scope tools/execution
```

Produce a capability-tier recommendation:

```shell
python3 -m tools.execution route \
  --factors path/to/routing-factors.json \
  --current-tier 2 \
  --execution-id EXEC-001 \
  --task-id STORY-001 \
  --scope tools/execution
```

These commands are focused Sprint 5.3 developer interfaces, not a general framework CLI.

## Execution Budget Architecture

A budget profile is supplied by a project or future execution profile. There is no universal global threshold.

```json
{
  "profile_id": "bounded-documentation-task",
  "limits": [
    {
      "dimension": "files_loaded",
      "threshold": 20,
      "action": "REQUIRE_JUSTIFICATION",
      "hard": false
    },
    {
      "dimension": "equivalent_failures",
      "threshold": 3,
      "action": "REQUEST_HUMAN",
      "hard": true
    }
  ]
}
```

Supported dimensions are:

- `files_loaded`
- `context_bytes`
- `context_expansions`
- `repository_traversals`
- `retrieval_operations`
- `tool_invocations`
- `execution_invocations`
- `retries`
- `equivalent_failures`
- `elapsed_duration_seconds`
- `tokens`

Token telemetry is optional. Missing values are reported as `UNAVAILABLE`, never inferred as zero.

Each configured limit declares a dimension, threshold, action, and soft or hard behavior. Actions are `WARN`, `CHECKPOINT`, `REASSESS`, `REQUIRE_JUSTIFICATION`, `ESCALATE`, `STOP`, and `REQUEST_HUMAN`.

Evaluation results are `WITHIN_BUDGET`, `SOFT_LIMIT`, `HARD_LIMIT`, `REASSESS_REQUIRED`, `HUMAN_REQUIRED`, or `UNAVAILABLE`. Every result records dimension, measured value, threshold, triggering event, response, and explanation.

Budget exhaustion never truncates required context, skips validation, hides evidence, or reduces mandatory review. The caller must checkpoint, reassess, justify expansion, escalate, stop, or request a person according to policy.

## Context-Manifest Integration

Budget evaluation can consume the existing Sprint 5.2 context manifest. It derives only deterministically available values:

- `files_loaded` from selected-file count;
- `context_expansions` from explicit nonzero expansion levels;
- restricted-context state; and
- fallback-required state.

It does not rebuild the repository index or duplicate selection. Measurements absent from the manifest remain unavailable.

## Checkpoint Architecture

The versioned JSON checkpoint records:

- repository commit, execution ID, task ID, objective, and scope;
- selected context, inspected and changed assets, and applicable standards;
- decisions, assumptions, evidence references, validation, and unresolved items;
- budget, retry, loop, routing, escalation, and execution state;
- restricted-context presence; and
- next recommended action.

The checkpoint stores identifiers, paths, categories, counts, hashes, and references rather than repository bodies, credentials, logs, or private data.

`CheckpointStore` writes, reads, validates, and evaluates resume compatibility. A matching commit and format returns `CURRENT_CHECKPOINT`. A changed repository commit or unsupported format returns `STALE_CHECKPOINT` and requires revalidation. It does not attempt a merge or silently resume against changed state.

Every serialized checkpoint declares `DERIVED_EXECUTION_STATE_NOT_APPROVAL`. A checkpoint is not an architecture decision, approval, exception, risk acceptance, production authorization, or release decision.

## Loop Detection

A failure event contains only:

- action type;
- command or tool identifier;
- normalized outcome;
- error category; and
- optional affected asset.

The detector normalizes case and whitespace and stores a bounded SHA-256 signature rather than raw output. Events with the same normalized signature are equivalent. A caller-supplied threshold controls when repetition becomes a loop; the framework defines no universal retry count.

Configured responses are `RETRY_ALLOWED`, `REASSESS`, `EXPAND_CONTEXT`, `ESCALATE_CAPABILITY`, `STOP`, and `REQUEST_HUMAN`. Below threshold, only `RETRY_ALLOWED` is returned. Crossing a threshold never causes an implicit retry or model invocation.

## Capability Routing

The core represents:

| Tier | Capability |
| --- | --- |
| 1 | Deterministic execution |
| 2 | Lightweight reasoning |
| 3 | General engineering reasoning |
| 4 | Advanced reasoning |
| 5 | Human or specialist authority |

Structured routing factors include task classification, complexity, change scope, security sensitivity, production impact, architecture significance, ambiguity, reversibility, reasoning depth, required tools, validation failures, equivalent failures, restricted context, hard budget pressure, and governed decision type.

The routing decision identifies current and recommended tier, reasons, triggering factors, mandatory escalation, human requirement, and `ESCALATE`, `DE_ESCALATE`, or `RETAIN` transition.

High complexity, ambiguity, sensitivity, impact, architecture significance, or reasoning need recommends Tier 4. Repeated lower-tier failure permits one bounded escalation. Deterministic work may de-escalate to Tier 1 after complex work is complete.

Architecture approval, risk acceptance, security exception, production authorization, release approval, and governance exception always require Tier 5. Tier 4 cannot substitute for Tier 5. Restricted required context also requires human authorization.

The routing contract can later be mapped to deterministic tools or appropriately governed lightweight, specialized, local, or hosted capabilities. This package contains no mapping, provider name, model name, SDK, quota logic, or execution adapter.

## Execution Evidence

Generated evidence records execution ID, repository commit, operation, budget evaluations, retries, loop evaluations, context expansions, restricted and fallback state, tier decisions, checkpoint references, and human-required state.

Context, budget, routing, loop, checkpoint, and validation artifacts share a small provenance envelope: evidence format/type, repository commit, optional index fingerprint, execution/task identity where applicable, UTC timestamp, runtime, operation, requested/effective scope, source asset, authority, and result. Unavailable optional fields are omitted rather than fabricated. Routing and loop commands require an execution ID and accept task/scope evidence; they contain no provider or model identity.

Checkpoints record creation timestamp and runtime in addition to their repository commit. Existing checkpoint fields and stale-commit behavior remain compatible. Validation report format 2.0 is preserved while exposing compatible common provenance fields.

Evidence is written beneath `.execution-reports/`, which is ignored by Git. Derived artifacts declare `DERIVED_EXECUTION_EVIDENCE_NOT_APPROVAL` in the common envelope. Checkpoints retain their more specific `DERIVED_EXECUTION_STATE_NOT_APPROVAL` marker as well. Evidence cannot approve work or suppress a failed control.

## Security, Privacy, and Anti-Gaming

- Do not include source bodies, credentials, sensitive logs, or personal data in profiles, signatures, checkpoints, or evidence.
- Preserve restricted-context and fallback state from the context manifest.
- Do not lower capability merely to conserve quota when risk requires a stronger tier or person.
- Do not hide retries, failures, context expansion, validation, evidence, or escalation.
- Do not skip standards, security review, or required validation to remain within budget.
- More resource use is correct when required for quality, security, privacy, evidence, or governance.

## Limitations and Deferred Work

- Profiles are caller-supplied; a governed execution-profile catalog is not implemented.
- State counters are updated from measured or supplied evidence; this package does not instrument external tools or models.
- Checkpoint reconciliation across repository commits is not implemented.
- Loop equivalence is intentionally limited to normalized structured events.
- No workflow/orchestration engine is included.
- Changed-file and affected-closure validation are implemented by `tools.validation`; full validation remains the release gate.
- No vendor routing, model invocation, local-model integration, adapter, playbook, workflow, or prompt catalog is included.
