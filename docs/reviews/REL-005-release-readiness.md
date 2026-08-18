# REL-005 Release Readiness and Governance Review Package

## Record Boundary

This package preserves original Sprint 5.5 evidence from repository commit `630c9ad` and the post-Architecture-remediation observation captured at commit `84d808a83c946cdd619ec3a7c449bc9d1b64c56b`. The current release-candidate and main commit after Documentation-remediation PR #33 is `837d9039f028ba57263a82d9e005a2b053352f7f`. Measurements dated 2026-08-10 are historical pre-Architecture-remediation observations and are not performance targets; the post-remediation context evidence below was generated at `84d808a` on 2026-08-12 and is not represented as measured at `837d903`. Automated results, routing recommendations, checkpoints, CI, and this package are evidence only; they do not approve architecture, security, documentation, domain, Product Owner, release, deployment, risk, or exceptions.

Risk classification is **Medium** because the change affects shared governance evidence and developer tooling but is reversible and has no production execution. Independent human review and complete automated validation are required.

## End-to-End Scenario

`tests/test_release_efficiency_governance.py` composes existing APIs with structured inputs and no AI model:

1. EFF-GOV-001 resolves through a fresh `RepositoryView` index.
2. `ContextSelector` produces an explainable manifest with task, release, epic, and sprint context.
3. `BudgetEvaluator` reports a configured hard threshold and unavailable token telemetry without removing controls.
4. `Router` recommends a conceptual capability tier.
5. Two equivalent structured validation failures trigger deterministic loop detection.
6. The release-approval factor routes Tier 4 to the human-only Tier 5.
7. `CheckpointStore` preserves state with `DERIVED_EXECUTION_STATE_NOT_APPROVAL` and verifies freshness.
8. Targeted validation emits provenance and preserves an error result as `FAIL` over selected and affected scope only.
9. Completion remains blocked pending accountable human decisions and full release validation.

Result: **PASS** for deterministic integration behavior; human escalation is the expected scenario outcome.

## Governance Invariant Evidence

| Invariant | Result and executable evidence |
| --- | --- |
| A. Under-contexting is not efficiency success | PASS. EFF-CTX-001 and EFF-MET-001 prohibit the claim; integration tests require completeness/fallback state and paired validation evidence. |
| B. Restricted required context forces fallback, authorization, or human escalation | PASS. Restricted mandatory release context sets incomplete/fallback state and routes to Tier 5. |
| C. Budget exhaustion cannot remove context, validation, or evidence | PASS. Budget results preserve an explicit required response and state that required controls must not be removed. |
| D. Tier 4 cannot satisfy Tier 5 | PASS. Release approval and risk acceptance recommend `HUMAN_SPECIALIST`; focused and integration tests cover Tier 4 input. |
| E. Checkpoint is not approval | PASS. Serialized authority is `DERIVED_EXECUTION_STATE_NOT_APPROVAL`. |
| F. Targeted validation cannot claim full validation | PASS. Mode and console coverage explicitly say selected and affected scope only. |
| G. Release closeout requires full validation | PASS. REL-005 policy, validation documentation, and this checklist require the default FULL command. |
| H. Stale index/checkpoint cannot silently resume | PASS. Stale indexes require fallback/refresh; stale checkpoints are incompatible and require revalidation. |
| I. Validation errors cannot be downgraded for resources | PASS. A targeted error fixture remains error severity, returns `FAIL`, and cannot be hidden by budget pressure. |
| J. Mandatory governance context cannot be optimized away | PASS. Required release context remains mandatory when restricted and forces fallback plus human authorization. |

## Efficiency Evidence Summary

### Historical Sprint 5.5 measurements

Representative local measurements from one pre-Architecture-remediation run on 2026-08-10:

| Evidence | Observed value |
| --- | ---: |
| Repository assets indexed | 84 |
| Repository source reads during index build | 84 |
| Index build elapsed | 131.193 ms |
| Targeted EFF-GOV-001 context files selected | 4 |
| Context-selection elapsed | 0.196 ms |
| Initial selection expansion levels | level 0 only |
| Full validation result-bearing assets | 73 |
| Targeted EFF-GOV-001 result-bearing assets | 25 |
| Full validation runner elapsed | 355.397 ms (runner report: 355 ms) |
| Targeted validation runner elapsed | 318.490 ms (runner report: 318 ms) |
| Budget evaluation | 0.076 ms |
| Checkpoint write / read | 0.236 ms / 0.065 ms |
| Routing decision | 0.015 ms |
| Loop evaluation | 0.054 ms |

The historical index read each metadata-bearing asset once per build. Before mandatory repository instructions were added to selector completeness, the representative targeted context set was 4 of 84 indexed assets. Targeted validation produced results for 25 assets versus 73 in full mode. These are historical measured file/scope observations, not token or universal performance claims. Global integrity validators still run in targeted mode, so runtime does not decrease in direct proportion to result-bearing assets.

### Current post-Architecture-remediation context evidence

In the post-Architecture-remediation observation captured at commit `84d808a83c946cdd619ec3a7c449bc9d1b64c56b`, `python3 -m tools.context select --story EFF-GOV-001` selected 5 files, with 0 restricted entries, 0 unresolved entries, no fallback, and `governing_context_complete: true`. The selected paths were:

- `AGENTS.md`
- `product/epics/EPIC-002-efficient-agentic-execution-context-engineering.md`
- `product/releases/REL-v0.5.md`
- `product/sprints/SPR-005-005-governance-release-closeout.md`
- `product/stories/EFF-GOV-001-governance-review-release-closeout.md`

The additional file is the mandatory root repository instruction introduced by the Architecture remediation. This current observation supplements rather than rewrites the original four-file measurement.

Context expansion is represented by explicit expansion levels and reasons; the representative initial selection needed no expansion. Restricted, unresolved, duplicate, stale, and governance-sensitive cases produce explicit fallback evidence. Eleven budget dimensions are supported: files, bytes, expansions, traversals, retrievals, tools, executions, retries, equivalent failures, duration, and optional tokens. Loop thresholds are caller-configurable and signatures are bounded hashes. Routing provides five conceptual tiers. Checkpoint resume verifies format and repository commit. Validation records runner elapsed time, validator set, scope, affected closure, fallback, result, and repository-read counts.

**Token savings: Not directly measured.** Token telemetry has not been supplied. v0.5 establishes mechanisms intended to reduce unnecessary context and model usage; it does not claim a percentage reduction.

## Success Assessment

REL-005 demonstrates smaller initial context by default, explainable selection, progressive expansion, configurable budgets, bounded retry, deterministic loop detection, capability escalation/de-escalation, explicit human-only Tier 5, durable checkpoints, targeted validation, full fallback, provenance, and vendor neutrality. Quality and governance remain prerequisites for efficiency success. Human review and release authorization are still pending, so the release is not closed.

## Vendor-Neutrality and Adapter Readiness

The audit searched v0.5 normative artifacts and implementation for named agent/model providers, proprietary token APIs, and provider SDK assumptions. Core code contains no provider SDK, product mapping, named model, model invocation, quota integration, or external execution adapter. Negative documentation statements about token APIs and vendor adapters describe exclusions and are acceptable.

The conceptual mapping remains feasible without core changes:

| Tier | Future adapter class |
| --- | --- |
| 1 | Deterministic or local tools |
| 2 | Local, small, or specialized AI |
| 3 | General engineering model |
| 4 | Advanced reasoning model |
| 5 | Accountable human or specialist |

No architectural barrier was found for future adapters because routing emits generic structured recommendations and does not execute capabilities. A future adapter contract, identity/provenance rules, privacy controls, telemetry translation, and execution boundary are intentionally absent and require separate governed design. Local execution cannot bypass security or privacy controls.

## Context-Efficiency Assessment

- Targeted selection is default-capable and begins with task/product context rather than repository bodies.
- Broader level-5 fallback occurs only when completeness evidence requires it or the caller explicitly requests it.
- Expansion levels and relationship paths make additions explainable.
- `.gitignore` exclusions are recorded and honored; explicit excluded targets become unresolved evidence.
- Restricted paths are separated from selected authorized context and force fallback.
- Manifests record commit, fingerprint, selected/restricted/unresolved paths, reasons, mandatory state, scope, exclusions, completeness, and fallback.

Gaps: semantic source-code dependency inference and governed restricted-path profiles are not implemented; callers supply targets and restricted patterns. Those limitations are visible rather than silently treated as complete.

## Budget and Routing Assessment

Soft/hard limits, explicit responses, unavailable values, configurable loop thresholds, bounded escalation, de-escalation, and Tier 5 authority are implemented. Hard pressure cannot lower capability or remove governance. Token usage is optional; model cost and model identity are not required or represented. Profiles and measurements remain caller-supplied because persistent orchestration and external execution are outside v0.5.

## Targeted Validation and Provenance Assessment

FULL is the default CLI and release-gate mode. Targeted modes expose requested/effective mode, direct scope, changed files, affected closure, ignored paths, and fallback. Repository-wide identity, relationship, catalog, traceability, lifecycle, and hygiene validators still execute. Schemas, templates, validator/registry code, validation workflows, core taxonomy/relationship authorities, standards catalog, and release-governance changes force full fallback. A targeted PASS is explicitly scoped and cannot certify the repository.

Validation evidence identifies repository/base/head commits, UTC timestamp, Python runtime, validator set, requested/effective mode, validation scope, changed paths, affected closure, ignored paths, fallback reasons, policy and repository fingerprints, counts, results, and elapsed time. Context evidence includes commit and content fingerprint; checkpoint/execution evidence includes commit, execution/task identity, authority markers, state, routing, loop, budget, and evidence references. Cryptographic signing is not required by current repository governance.

## v0.4 Finding Dispositions

| Finding | REL-005 classification | Evidence / remaining boundary |
| --- | --- | --- |
| ARCH-REL004-002 | CLOSED BY REL-005 | Product metadata contracts and ID formats are executable through `VAL-META-001` and traceability checks. |
| ARCH-REL004-003 | CLOSED BY REL-005 | EFF-MET-001 defines semantics; validation report v2 provides rich provenance and explicit count meanings. |
| ARCH-REL004-004 | CLOSED BY REL-005 | Registry identity/uniqueness and unexpected-validator-exception tests are implemented. |
| ARCH-REL004-006 | PARTIALLY ADDRESSED | Shared RepositoryView and changed/affected execution exist; broader validator adoption and semantic source dependencies remain future work. |
| DOM-REL004-001 | CLOSED BY REL-005 | Release, epic, sprint, story, architecture contracts, and tool packages identify accountable owners/boundaries. |
| DOM-REL004-003 | PARTIALLY ADDRESSED | EFF-MET-001 and machine evidence share execution terms; broader cross-standard taxonomy harmonization remains future work. |
| SEC-REL004-003 | CLOSED BY REL-005 | Root `SECURITY.md` now supplies repository guidance without inventing disclosure contacts. |
| SEC-REL004-005 | CLOSED BY REL-005 | Validation report v2 records attributable provenance and scope; signing is not required. |
| SEC-REL004-006 | PARTIALLY ADDRESSED | Targeted scope, single index reads, bounded failure signatures, fixed Git arguments, and exception evidence improve robustness; universal validator resource limits are not policy. |

The v0.4 release artifact and its accepted-risk record are unchanged.

## Remaining REL-005 Gaps

| Gap | Disposition |
| --- | --- |
| Broader RepositoryView adoption | v0.6 candidate |
| Semantic source-code dependency inference | future backlog |
| Governed restricted-path profiles | v0.6 candidate |
| Cryptographic evidence signing | not required |
| Vendor adapter mappings | future backlog |
| Actual token/cost telemetry | future backlog |
| Persistent execution orchestration | future backlog |
| External-model execution | future backlog |
| Cross-session runtime and checkpoint reconciliation | future backlog |
| Hosted CI result for the Sprint 5.5 and Architecture-remediation PRs | satisfied; Framework Validation passed before merge |
| Branch protection and workflow ownership verification | administrative |

## Security and Privacy Review Evidence

Review scope: `tools/context`, `tools/execution`, and `tools/validation`.

- Path traversal: context targets and Markdown targets resolve beneath the root; shared repository containment rejects context, execution, and validation CLI evidence paths whose absolute, parent-traversal, or symlink-resolved target escapes the repository.
- Subprocess safety: Git calls use fixed argument arrays, no shell, captured output, and explicit working directories.
- Sensitive evidence: indexes contain metadata, checkpoints use identifiers/references, loop events store hashes, and guidance prohibits bodies/secrets/private logs. Generated evidence remains ignored.
- Restricted context: selection separates restricted entries and routing requires Tier 5 authorization.
- Stale reuse: index fingerprint/commit and checkpoint format/commit checks prevent silent governed resume.
- Arbitrary loading: context, execution, and validation CLI evidence paths are repository-contained; library APIs remain explicit trusted-caller interfaces.
- Vendor coupling and dynamic execution: no SDK, model invocation, dynamic plugin loading, `eval`, or `exec` exists. YAML scalar handling uses `ast.literal_eval`, not dynamic evaluation.
- Deserialization: JSON and a repository-defined YAML subset are used; no pickle or unsafe object deserializer exists.

Findings remediated: Sprint 5.5 added execution CLI path containment; SEC-REL005-001 extends the same boundary consistently to context and validation CLI evidence paths through a small shared helper. Focused tests cover valid repository-relative and nested paths, absolute outside paths, parent traversal, symlink escape, context index input/output, context-manifest output, validation-report output, and the existing execution boundary. The authorized human decision below accepts the remaining visible risks without representing them as remediated or closed.

### Security Review Decision

Decision: **APPROVED WITH ACCEPTED RESIDUAL RISK**. The authorized human decision is based on merged-main commit `005263090fb7641a654e6cfa556948ab57f001ff`: FULL validation PASS, 139 tests PASS, focused path-security tests PASS, hosted Framework Validation CI PASS, `main == origin/main`, and a clean working tree. No reviewer identity, signature, credentials, or timestamp is inferred.

| Finding | Authorized disposition | Evidence / residual boundary |
| --- | --- | --- |
| SEC-REL005-001 | Condition Satisfied | Shared containment resolves paths and rejects absolute, parent-traversal, or symlink-resolved targets outside the repository without rewriting them. Context `--index`/`--output`, validation `--report`, and execution evidence paths use the common boundary and return deterministic CLI error status 2 for unsafe paths. |
| SEC-REL004-001 | Accepted/Deferred | Branch-protection enforcement remains administratively unverified. |
| SEC-REL004-002 | Accepted/Deferred | Repository-owned secret scanning remains absent. |
| SEC-REL004-004 | Accepted/Deferred | CODEOWNERS and checkout-credential hardening remain future repository-administration work. |
| SEC-REL004-006 | Accepted as partially addressed | Targeted scope, bounded signatures, fixed Git commands, exception evidence, and CI timeout improve robustness; broader resource controls remain future hardening. |
| SEC-REL005-002 | Accepted/Deferred | Governed restriction profiles remain future hardening; current restrictions are caller-supplied and relevance does not authorize access. |
| SEC-REL005-003 | Accepted/Deferred | Broader resource and input-size controls remain future hardening. |
| SEC-REL005-004 | Accepted residual risk | Automated filtering of caller-supplied sensitive evidence remains future hardening; minimization guidance and ignored evidence directories remain required controls. |

These accepted and deferred findings remain open and visible. Approval does not describe them as remediated or closed and does not authorize Product Owner acceptance, release, production action, or a tag.

## Test Completeness

The suite covers happy/failure paths, index freshness, restricted context, budget exhaustion and unavailable telemetry, loop thresholds/signatures, human-only routing, de-escalation, targeted fallback, provenance, registry uniqueness, validator exceptions, and CLI path containment. The end-to-end integration test covers cross-component composition. Remaining gaps align with out-of-scope persistent orchestration, external execution, semantic code dependency inference, and cross-session reconciliation.

## EFF-CTX-001 Acceptance Review

| Principle | Assessment | Evidence |
| --- | --- | --- |
| Context minimization | IMPLEMENTED | Default selector starts with Minimum Sufficient Context and selected 4 of 84 indexed assets in the representative run. |
| Progressive context loading | IMPLEMENTED | Levels 0–5 and evidence-backed fallback/expansion are executable. |
| Task isolation | IMPLEMENTED | Manifest and checkpoint bind one task/objective/scope; bounded-execution contract prohibits unrelated work. |
| Model/capability tiering | IMPLEMENTED | Generic Tier 1–5 router with escalation, de-escalation, and Tier 5 authority. |
| Context reuse | PARTIALLY IMPLEMENTED | Durable index/manifests/checkpoints exist; cross-session reconciliation and runtime orchestration do not. |
| Repository hygiene | IMPLEMENTED | Exclusions, generated-evidence ignores, tracked-artifact checks, and 15 Draft standards remain preserved. |
| Evidence over conversation | IMPLEMENTED | Structured manifests, execution evidence, checkpoints, and validation report v2. |
| Loop detection | IMPLEMENTED | Deterministic normalized hashed signatures and configurable threshold/response. |
| Summary checkpoints | IMPLEMENTED | Versioned durable checkpoint with freshness and non-approval marker. |
| Local/lightweight routing readiness | IMPLEMENTED | Generic tiers accept future mappings without core vendor dependencies; mappings remain intentionally absent. |

## EFF-MET-001 Acceptance Review

| Measurement | Support |
| --- | --- |
| Context files | Measured in selection manifest and budget state. |
| Context bytes | Supported budget dimension; unavailable unless supplied. |
| Retrievals | Retrieval-operation and repository-traversal dimensions supported; instrumentation is caller-supplied. |
| Expansions | Manifest levels and execution evidence count explicit expansions. |
| Repeated scans | Index source-read count and repository traversal dimension; cross-run aggregation is not implemented. |
| Tool calls | Supported dimension; caller supplies measured state. |
| Executions | Supported dimension; caller supplies measured state. |
| Retries | Budget/checkpoint/evidence fields. |
| Equivalent failures | Deterministic loop signatures, counts, and thresholds. |
| Duration | Index generation, validation runner, and supported execution duration dimension. |
| Routing transitions | Structured current/recommended tier, reasons, factors, and transition. |
| Checkpoint/resume | Current/stale result and revalidation requirement. |
| Validation scope | Requested/effective mode, direct/affected scope, fallback, and result counts. |
| Optional tokens | Supported and explicitly `UNAVAILABLE` when absent. |

Anti-gaming controls are documented and executable at the relevant boundaries: incomplete/restricted/stale state forces fallback, budget messages preserve controls, errors retain severity, Tier 5 is non-substitutable, and targeted results expose limited coverage.

## Human Review Packages

| Review | Status | Evidence prepared / required decision |
| --- | --- | --- |
| Architecture Review | Approved — Conditions Satisfied | Human Architecture Reviewer | The authorized human decision records Architecture Review as Approved and ARCH-REL005-001 and ARCH-REL005-002 as Conditions Satisfied. Remaining Architecture findings stay non-blocking/future debt. No reviewer identity, signature, credentials, or timestamp is inferred. |
| Domain Review | Approved — DOM-REL005-001 Condition Satisfied | Human Domain Reviewer | The authorized human decision records Domain Review as Approved based on merged-main commit `c695bf65eb67fc2a8ce75e4efa68b8b03f7fc10a`: FULL validation PASS, 131 tests PASS, focused context tests PASS, hosted Framework Validation CI PASS, `main == origin/main`, and a clean working tree. No reviewer identity, signature, credentials, or timestamp is inferred. |
| Documentation Review | Approved — Conditions Satisfied | Human Documentation Reviewer | The authorized human decision records Documentation Review as Approved and DOC-REL005-001 through DOC-REL005-006 as Conditions Satisfied. No reviewer identity, signature, credentials, or timestamp is inferred. |
| Security Review | Approved with Accepted Residual Risk | The authorized human decision records SEC-REL005-001 as Condition Satisfied and explicitly accepts or defers the visible residual findings listed in the Security Review Decision. No reviewer identity, signature, credentials, or timestamp is inferred. |
| Product Owner | Pending | Decide story/sprint acceptance and release readiness after other evidence and hosted CI are available. |

## Release-Readiness Checklist

- [ ] Sprint 5.1 human approval complete (implementation is complete and In Review)
- [ ] Sprint 5.2 human approval complete (implementation is complete and In Review)
- [ ] Sprint 5.3 human approval complete (implementation is complete and In Review)
- [ ] Sprint 5.4 human approval complete (implementation is complete and In Review)
- [x] Sprint 5.5 implementation complete
- [x] All eight stories reviewed for implementation evidence
- [x] FULL local validation PASS
- [x] Complete local test suite PASS
- [x] Hosted Framework Validation CI PASS for merged Sprint 5.5 and Architecture-remediation changes
- [x] Vendor-neutrality assessment prepared
- [x] Security/privacy assessment prepared
- [x] Documentation assessment prepared
- [x] Architecture Review approved
- [x] Domain Review approved
- [x] Documentation Review approved
- [x] Security Review approved
- [ ] Product Owner approval
- [x] Known gaps dispositioned
- [ ] Release date recorded
- [ ] v0.5 tag created after authorization

REL-005 and EPIC-002 remain **In Progress**. EFF-GOV-001 and all prior EFF stories remain **In Review**. The recorded review decisions do not imply Product Owner approval, lifecycle completion, release authorization, or a tag.

## Architecture Review Decision

Decision: **APPROVED**. The authorized human decision confirms that ARCH-REL005-001 and ARCH-REL005-002 are satisfied. No reviewer identity, signature, credentials, or timestamp is inferred.

| Finding | Implementation disposition | Evidence |
| --- | --- | --- |
| ARCH-REL005-001 | Condition Satisfied | Context selection includes the actual mandatory root `AGENTS.md` instruction directly, reports repository-instruction, task-governance, applicable-standard, restricted-governance, and aggregate completeness, and forces fallback for missing or restricted mandatory governance. No upstream-preload assumption is used. |
| ARCH-REL005-002 | Condition Satisfied | A small shared provenance helper supplies evidence type/version, commit/fingerprint, execution/task identity, UTC time, runtime, operation, requested/effective scope, source asset, non-approval authority, and result across context and execution evidence. Checkpoint freshness remains unchanged and validation report 2.0 remains backward compatible. |

Non-blocking findings remain tracked without implementation in this remediation: ARCH-REL005-003 common path containment, ARCH-REL005-004 generic future-release fallback, ARCH-REL005-005 alternating-cycle detection, and ARCH-REL005-006 broader RepositoryView/adapters/orchestration work.

## Documentation Review Decision

Decision: **APPROVED**. The authorized human decision confirms that DOC-REL005-001 through DOC-REL005-006 are satisfied. No reviewer identity, signature, credentials, or timestamp is inferred.

| Finding | Authorized disposition |
| --- | --- |
| DOC-REL005-001 | Condition Satisfied |
| DOC-REL005-002 | Condition Satisfied |
| DOC-REL005-003 | Condition Satisfied |
| DOC-REL005-004 | Condition Satisfied |
| DOC-REL005-005 | Condition Satisfied |
| DOC-REL005-006 | Condition Satisfied |

## Domain Review Conditional Remediation

Decision: **APPROVED**. The authorized human decision confirms that DOM-REL005-001 is satisfied. It is based on merged-main commit `c695bf65eb67fc2a8ce75e4efa68b8b03f7fc10a` and the confirmed evidence: FULL validation PASS, 131 tests PASS, focused context tests PASS, hosted Framework Validation CI PASS, `main == origin/main`, and a clean working tree. No reviewer identity, signature, credentials, or timestamp is inferred.

| Finding | Implementation disposition | Evidence |
| --- | --- | --- |
| DOM-REL005-001 | Condition Satisfied | Context-manifest provenance reports overall selection sufficiency: `COMPLETE` only when no fallback is required, otherwise `FALLBACK_REQUIRED`. Detailed repository, standard, task, restricted-governance, and aggregate governing-context indicators remain independent. Focused tests cover sufficient context, unresolved dependencies with complete governance, restricted context, missing governance, stale/fallback state, and the non-approval authority marker. |

This remediation does not advance Security Review, Product Owner approval, story or sprint lifecycle, EPIC-002, or REL-005 release status.
