# Repository Index and Targeted Context

## Purpose

`tools.context` implements EFF-IDX-001 and EFF-SEL-001 as a dependency-free, deterministic repository intelligence layer. It builds a metadata-only view of governed assets and selects explainable Minimum Sufficient Context before any AI or model invocation.

The repository remains authoritative. The index is generated evidence and MUST NOT override repository files, schemas, templates, the [asset taxonomy](../../docs/framework/FRAMEWORK_ASSETS.md), the [relationship model](../../docs/architecture/CROSS_REFERENCE_MODEL.md), or product records.

## Local Commands

Build or rebuild the index:

```shell
python3 -m tools.context index
```

Select context for a story:

```shell
python3 -m tools.context select --story EFF-IDX-001
```

Select context for an asset and explicit target:

```shell
python3 -m tools.context select --asset STD-API-001 --target standards/api/STD-API-001-api-design-standard.md
```

Mark a relevant path as restricted without authorizing access:

```shell
python3 -m tools.context select --story EFF-SEL-001 --restricted-path 'restricted/**'
```

Use `--expand-to 0` through `--expand-to 5` to set the requested progressive expansion boundary. `--full-fallback` includes all indexed governed assets when deterministic completeness checks require fallback. This is repository context tooling, not the future general framework CLI.

## Repository View and Index

The builder uses the validation framework's YAML-subset frontmatter parser and Markdown link resolver. It reads each metadata-bearing Markdown asset once per build and emits deterministic ordering for:

- framework ID, asset type, title, path, lifecycle status, owner, release, epic, and sprint;
- parent, standard, supersedes, link, and deliverable relationships that existing repository artifacts express;
- validation-relevance categories; and
- unresolved relationships and duplicate identities.

The index stores metadata, paths, and relationships—not document bodies. It is regenerable and is not manually maintained.

## Format and Provenance

The JSON index records:

- index format version;
- source commit SHA;
- governed-source fingerprint;
- generation time;
- repository-relative root;
- assets, relationships, duplicates, unresolved items, and exclusions; and
- files inspected, metadata files parsed, assets, relationships, source reads, and generation duration.

The source fingerprint covers the paths and content of indexed governed files. An index is stale when its format, commit, or fingerprint differs from the current repository. The `select` command safely regenerates a missing or stale local index before selection. Library consumers receive explicit freshness state and must not silently use stale data for governed decisions.

Default evidence locations are:

```text
.context-reports/repository-index.json
.context-reports/context-manifest.json
```

`.context-reports/` is ignored by Git. Generated evidence must not be committed unless a later governed process explicitly requires a retained artifact.

## Progressive Selection

The selector uses explicit levels aligned with the [Sprint 5.1 contract](../../docs/architecture/EXECUTION_EFFICIENCY_CONTEXT_MANAGEMENT.md):

| Level | Context |
| --- | --- |
| 0 | Task, release, epic, and sprint context |
| 1 | Explicitly related standards and governing architecture/governance documents |
| 2 | Explicit target paths or governed assets |
| 3 | Direct metadata, link, and deliverable dependencies |
| 4 | Assets that directly reference selected seeds |
| 5 | Broader governed-asset fallback when requested and required |

The root `AGENTS.md` is the repository's mandatory implementation-agent instruction source and is selected directly at level 0. It is not added to the metadata index and its body is not copied into derived evidence. Release, epic, sprint, story, explicitly applicable standards, and linked governance or architecture assets provide task-specific governing context.

Selection uses declared repository relationships. It does not perform semantic dependency inference, call an AI model, use token APIs, or hard-code a universal standard set.

## Context Manifest

The JSON manifest explains:

- repository commit and index fingerprint;
- task reference and explicit targets;
- selected path, asset ID, context category, reason, relationship path, source ID, mandatory state, restriction state, and expansion level;
- restricted and unresolved context;
- active repository exclusions;
- deterministic completeness indicators;
- fallback requirement and reasons; and
- selected, restricted, excluded, unresolved, expansion-level, and fallback counts.

Completeness uses explainable booleans such as target resolved, dependencies resolved, index fresh, and restricted required context clear. It does not manufacture probabilistic confidence.

Governing completeness separately reports repository instructions, task governance, applicable standards, restricted governance, and the aggregate `governing_context_complete`. The aggregate is true only when the mandatory root instruction exists and is authorized, the task hierarchy resolves, applicable standards at the active expansion level are selected, and no mandatory governance item is restricted. Missing or restricted mandatory governance forces fallback and cannot be represented as a normal complete result.

The manifest also carries a common non-approval provenance envelope with evidence type/version, commit and index fingerprint, UTC generation time, runtime, operation, requested/effective scope, source task, authority, and completeness result.

## Exclusions

The index reads only metadata-bearing governed Markdown assets. Selection exclusions are derived from `.gitignore`, plus the mandatory `.git/` boundary. This excludes generated validation/context reports, caches, and bytecode under current repository conventions without hiding governed product or standards content.

An explicit target excluded by repository policy is reported as unresolved and forces fallback rather than being silently ignored.

## Restricted Context

Restriction patterns are supplied by an authorized caller or future execution profile. The repository currently has no governed enterprise sensitivity catalog, so the tool does not invent one.

Relevant restricted context is recorded as `REQUIRED BUT RESTRICTED`, removed from the authorized selected set, and causes fallback or human authorization to be required. Relevance never grants access. The index never stores sensitive file bodies.

## Fallback

Fallback is required for unresolved task or target identity, unresolved direct dependency, stale index, duplicate identity, excluded explicit target, or required restricted context. Callers may also require broader review for security, architecture, validation, or governance reasons not deterministically encoded in this Sprint 5.2 selector.

The selector reports fallback; it does not approve access or make a human governance decision. When `--full-fallback` is used, only indexed governed assets are broadened automatically, and restricted assets remain restricted.

## Limitations and Deferred Work

- At the completion of Sprint 5.2, broader validator reuse, execution governance, and targeted validation remained assigned to later v0.5 sprints. The current release candidate now composes the independently usable layers: Sprint 5.2 provides indexing and context selection; Sprint 5.3 provides budgets, checkpoints, loop controls, and routing; Sprint 5.4 provides targeted validation and provenance; and Sprint 5.5 provides integration and governance evidence.
- RepositoryView is reused for targeted planning and framework-ID integrity; broader adoption by every repository-wide validator remains an incremental opportunity.
- Relationship discovery is explicit and deterministic; it does not infer semantic source-code dependencies.
- Restricted-path policy must be supplied by an authorized caller until a governed execution-profile mechanism exists.
- Context tooling remains independently usable and does not orchestrate the execution or validation layers.
- The tool has no model SDK, routing, local-model, vendor-adapter, prompt, playbook, or workflow dependency.

## Governance Boundary

Index or context evidence cannot accept risk, authorize restricted access, approve an exception, waive a standard, suppress validation, approve architecture or security, authorize deployment, authorize release, or impersonate human approval.
