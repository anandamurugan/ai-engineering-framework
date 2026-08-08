# Validation Framework Foundation

This directory contains the repository-owned, vendor-neutral execution foundation for deterministic validation. It produces evidence; it does not confer approval or modify governed artifacts.

## Run locally

From the repository root, run:

```sh
python3 -m tools.validation
```

The command executes the statically registered validators, prints a concise summary, writes `.validation-reports/validation-report.json`, and returns `0` when no error-severity check fails. An error failure returns `1`. Warning failures remain visible but do not make the run fail.

Use `--root PATH` to validate an explicitly selected repository root or `--report PATH` to select another report path. Relative report paths are resolved from the repository root. The default report directory is ignored by Git.

## Contract and registry

A validator extends `Validator`, declares `validator_id`, `name`, `description`, and `default_severity`, and implements `validate(context)`. It returns one or more immutable `ValidationResult` values containing:

- validator ID;
- name and description;
- status (`PASS` or `FAIL`);
- severity (`ERROR`, `WARNING`, or `INFO`);
- affected file or asset when available; and
- an attributable message.

Add an approved validator by importing and instantiating it in `registry.py`. Registration is intentionally explicit: this foundation has no dynamic discovery or plugin runtime.

## Reporting

The JSON report contains `report_version`, aggregate `summary`, and structured `results`. The summary records validators executed, unique assets scanned, errors, warnings, passed checks, and overall `PASS` or `FAIL`. Each result includes the validator, status, severity, asset, framework ID when available, and message.

## Registered validation

- `VAL-FWK-SELF-001` verifies repository-root resolution and registry loading.
- `VAL-META-001` validates release, epic, sprint, and story metadata against the contracts in the Framework Asset Taxonomy. It validates standard front matter directly against `schemas/standard.schema.yaml`, including required and additional properties, types, controlled values, patterns, lengths, unique arrays, and date formats.
- `VAL-META-ID-001` detects duplicate IDs across all metadata-bearing Markdown files and reports every conflicting file. Defined product and standard ID formats are enforced by `VAL-META-001`.
- `VAL-STRUCT-001` derives the required standard sections and order from `templates/standard-template.md`. It also checks H1 identity, duplicate sections, numbered mandatory-rule presence, and the revision-history table structure.

An error finding makes the command return `1`; findings remain in console and JSON evidence. Conformance never implies substantive review or approval. Metadata contracts for asset types without an executable schema are not inferred by this milestone.

The implementation uses no third-party dependencies. Its YAML reader supports the mapping, sequence, and scalar forms used by current repository front matter and the standard schema; it is not a general-purpose YAML implementation.

Link and cross-reference validation, catalog parity, lifecycle traceability, repository hygiene, Markdown lint integration, and CI integration remain intentionally deferred to their approved Sprint 4.4 stories.

## Governance boundaries

Validation is read-only evidence-producing automation. It MUST NOT approve standards or architecture, accept risk, approve exceptions, deployments, or releases, alter governed artifacts merely to pass, or replace Product Owner review. A successful run establishes only that registered checks passed. A failed control cannot be suppressed or represented as passed.

AI may analyze failures, recommend corrections, draft remediation, and summarize evidence. AI must not suppress failures, falsify evidence, change thresholds without governed approval, mark a failed control as passed, or approve governance exceptions.

## Tests

Run the standard-library test suite from the repository root:

```sh
python3 -m unittest discover -s tests
```
