# Validation Framework Foundation

This directory contains the repository-owned, vendor-neutral execution foundation for deterministic validation. It produces evidence; it does not confer approval or modify governed artifacts.

## Run locally

From the repository root, run:

```sh
python3 -m tools.validation
```

The command executes the statically registered validators, prints a concise summary, writes `.validation-reports/validation-report.json`, and returns `0` when no error-severity check fails. An error failure returns `1`. Warning failures remain visible but do not make the run fail.

Use `--root PATH` to validate an explicitly selected repository root or `--report PATH` to select another report path. Relative report paths are resolved from the repository root. The default report directory is ignored by Git.

Full validation remains the default:

```sh
python3 -m tools.validation
```

Targeted modes are explicit:

```sh
python3 -m tools.validation --mode asset --asset EFF-VAL-001
python3 -m tools.validation --mode affected --base main --head HEAD
python3 -m tools.validation --mode changed --working-tree
python3 -m tools.validation --mode asset --paths product/stories/EFF-VAL-001-targeted-validation-evidence-provenance.md
```

The modes are `FULL`, `TARGETED_ASSET`, `CHANGED_FILES`, and `AFFECTED_CLOSURE`. Git discovery uses fixed subprocess argument arrays and supports working-tree changes or a base/head range. Added, deleted, modified, and renamed paths are retained as evidence; ignored generated paths are excluded.

Targeted planning maps changed paths and framework IDs through the derived Sprint 5.2 `RepositoryView`. The affected closure follows authoritative product parents, story deliverables, standard relationships, and their reverse references. It does not infer semantic source-code dependencies. Unknown paths, stale or ambiguous indexes, duplicate identities, schemas, templates, validator code or registry changes, validation workflows, taxonomy/relationship authorities, standards catalog changes, and release-governance changes force full validation.

A targeted `PASS` covers only the selected and affected scope. Repository-wide validators still execute to preserve ID, relationship, catalog, traceability, lifecycle, and hygiene integrity. Targetable metadata, structure, and local-link checks receive the affected file scope. REL-005 release closeout MUST use full validation unless a future explicit governance decision changes that rule.

## Contract and registry

A validator extends `Validator`, declares `validator_id`, `name`, `description`, `default_severity`, and a `scope_capability` of `TARGETABLE` or `REPOSITORY_WIDE`, then implements `validate(context)`. It returns one or more immutable `ValidationResult` values containing:

- validator ID;
- name and description;
- status (`PASS` or `FAIL`);
- severity (`ERROR`, `WARNING`, or `INFO`);
- affected file or asset when available; and
- an attributable message.

Add an approved validator by importing and instantiating it in `registry.py`. Registration is intentionally explicit: this foundation has no dynamic discovery or plugin runtime. Registry integrity rejects missing identities, non-validator entries, and duplicate validator IDs before execution.

## Reporting

JSON report format `2.0` contains `provenance`, an aggregate `summary`, and structured `results`. Provenance records repository/base/head revisions, governed-content fingerprint, UTC execution time, Python runtime identity and version, executed validator IDs, requested and effective modes, selected paths, affected closure, ignored paths, fallback reasons, and a registry-policy fingerprint. Each result includes the validator, status, severity, asset, framework ID when available, and message. Unexpected validator exceptions become error-severity evidence without printing a traceback or falsely producing success.

Count semantics are explicit: `validators_executed` counts registered checks invoked; `governed_assets_evaluated` counts distinct result assets; `scoped_assets` counts directly requested paths; `affected_assets` counts the expanded closure; `repository_files_inspected` and `repository_source_reads` describe RepositoryView construction; `passed_checks` counts passing result records; and `findings` counts all failed result records, including advisory warnings. `elapsed_ms` measures runner execution and does not include Git discovery or index construction.

## Registered validation

- `VAL-FWK-SELF-001` verifies repository-root resolution and registry loading.
- `VAL-META-001` validates release, epic, sprint, and story metadata against the contracts in the Framework Asset Taxonomy. It validates standard front matter directly against `schemas/standard.schema.yaml`, including required and additional properties, types, controlled values, patterns, lengths, unique arrays, and date formats.
- `VAL-META-ID-001` detects duplicate IDs across all metadata-bearing Markdown files and reports every conflicting file. Defined product and standard ID formats are enforced by `VAL-META-001`.
- `VAL-STRUCT-001` derives the required standard sections and order from `templates/standard-template.md`. It also checks H1 identity, duplicate sections, numbered mandatory-rule presence, and the revision-history table structure.
- `VAL-REF-LINK-001` checks repository-relative Markdown paths with exact filename case, `../` resolution, URL-decoding, and local heading fragments. External URI schemes are excluded.
- `VAL-REF-STD-001` checks standard relationship targets, matching navigation, prohibited directional cycles, and optional reciprocity. Missing optional `related_standards` reciprocity is a warning; conceptual cycles are permitted.
- `VAL-TRACE-CATALOG-001` compares every catalog row with the standard ID, title, category, version, status, owner, mandatory flag, and path.
- `VAL-TRACE-PRODUCT-001` checks release, epic, sprint, and story parents; parent tracking tables; story deliverables; and the explicit rule that a completed sprint cannot contain incomplete tracked stories.
- `VAL-HYGIENE-PLACEHOLDER-001` detects case-insensitive `TODO`, `TBD`, `FIXME`, `PLACEHOLDER`, `Lorem ipsum`, and `coming soon` markers in governed text.
- `VAL-HYGIENE-WHITESPACE-001` reports trailing spaces or tabs with file and line evidence across repository text files.
- `VAL-HYGIENE-MARKDOWN-001` checks one H1, heading-level progression, empty or malformed headings, and balanced fenced code blocks without duplicating standard-section validation.
- `VAL-HYGIENE-ARTIFACT-001` rejects tracked validation reports, Python caches, and compiled Python files using the repository's `.gitignore` conventions.

An error finding makes the command return `1`; findings remain in console and JSON evidence. Conformance never implies substantive review or approval. Metadata contracts for asset types without an executable schema are not inferred by this milestone.

The implementation uses no third-party dependencies. Its YAML reader supports the mapping, sequence, and scalar forms used by current repository front matter and the standard schema; it is not a general-purpose YAML implementation.

Findings name the source asset, framework ID, target, relationship type, and reason where applicable. For example: `EPIC-001 -> SPR-004-404 (contains): tracked child is missing or does not belong to this parent.` External-site availability, generalized future relationship schemas, subjective relationship meaning, and lifecycle rules not stated by repository policy are excluded.

Placeholder exclusions are intentionally narrow: `templates/` authoring markers, `tests/` fixtures, historical `CHANGELOG.md` text, validation and style-guide explanations, the VAL-HYGIENE-001 specification, explicitly explanatory planning statements, and REL-004's Product Owner-owned `target_release: TBD`. Generated reports and cache directories are excluded from content scans but fail artifact hygiene if Git tracks them.

No supported Markdown linter dependency or configuration exists, so CI runs the deterministic repository-defined Markdown hygiene checks rather than adding a separate toolchain. VAL-GOV-001 implementation is complete, but no repository-owned secret scanner exists. The Security Reviewer accepted and deferred the gap for v0.4.0 without representing it as remediated; the external commit hook remains supplemental evidence and is not repository CI enforcement.

Sprint 4.4 implementation and governance closeout evidence are recorded in [SPR-004-004](../../product/sprints/SPR-004-004-governance-validation.md). Architecture, Domain, Documentation, Security, and Product Owner decisions are recorded there. Human governance gates are not satisfied by validator or CI success.

The current implementation intentionally has no dedicated Markdown linter or repository-owned secret scanner, and branch protection remains unverified. Product asset types other than standards do not yet have executable schemas; their current contracts are derived from the [Framework Asset Taxonomy](../../docs/framework/FRAMEWORK_ASSETS.md). The shared repository view now supplies framework-ID integrity and targeted planning; broader adoption by every repository-wide validator remains an incremental efficiency opportunity.

## Continuous integration

`.github/workflows/framework-validation.yml` runs for pull requests targeting `main`, pushes to `main`, and manual dispatches. It uses Python 3.9 with no third-party dependencies and executes the same framework command and standard-library test suite documented here. Both commands run even if one fails, the final enforcement step fails the job on either failure, and warnings remain visible without being converted into errors.

The workflow uploads `.validation-reports/validation-report.json` as the `framework-validation-report` artifact for 14 days, including after validation failure when a report was produced. Reports remain ignored by Git. Reproduce CI locally with:

```sh
python3 -m tools.validation
python3 -m unittest discover -s tests
```

For protected branches, a repository administrator should configure `Framework Validation / Framework validation` as a required status check. The workflow does not enable branch protection or approve a pull request; a successful check is conformance evidence only and human approval remains mandatory.

When CI fails, inspect the validation step summary and download the JSON artifact for file-level findings. Re-run both local commands from the repository root. If the report is absent, inspect the runner setup and import failure before treating the result as validation evidence.

## Governance boundaries

Validation is read-only evidence-producing automation. It MUST NOT approve standards or architecture, accept risk, approve exceptions, deployments, or releases, alter governed artifacts merely to pass, or replace Product Owner review. A successful run establishes only that registered checks passed. A failed control cannot be suppressed or represented as passed.

AI may analyze failures, recommend corrections, draft remediation, and summarize evidence. AI must not suppress failures, falsify evidence, change thresholds without governed approval, mark a failed control as passed, or approve governance exceptions.

## Tests

Run the standard-library test suite from the repository root:

```sh
python3 -m unittest discover -s tests
```
