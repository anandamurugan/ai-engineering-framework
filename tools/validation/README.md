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

The JSON report contains `report_version`, aggregate `summary`, and structured `results`. The summary records validators executed, unique assets scanned, errors, warnings, passed checks, and overall `PASS` or `FAIL`. Later validators should use the same model so local and CI evidence stays consistent.

The only registered check in this foundation verifies repository-root resolution and registry loading. Metadata, IDs, document structure, links, cross-references, catalog parity, traceability, repository hygiene, Markdown lint integration, and lifecycle governance checks remain intentionally deferred to their approved Sprint 4.4 stories.

## Governance boundaries

Validation is read-only evidence-producing automation. It MUST NOT approve standards or architecture, accept risk, approve exceptions, deployments, or releases, alter governed artifacts merely to pass, or replace Product Owner review. A successful run establishes only that registered checks passed. A failed control cannot be suppressed or represented as passed.

AI may analyze failures, recommend corrections, draft remediation, and summarize evidence. AI must not suppress failures, falsify evidence, change thresholds without governed approval, mark a failed control as passed, or approve governance exceptions.

## Tests

Run the standard-library test suite from the repository root:

```sh
python3 -m unittest discover -s tests -p 'test_validation_foundation.py'
```
