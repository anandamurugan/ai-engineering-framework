---
id: architecture.release-model
title: Release Model
version: 0.2.0
status: proposed
owner: Framework Maintainers
tags:
  - architecture
  - release
  - compatibility
ai_consumable: true
human_reviewed: false
last_updated: 2026-07-23
---

# Release Model

## Purpose and current state

This model defines how the framework itself should be versioned, reviewed, released, supported, and recovered. It is a proposed process. The repository currently has no automated release pipeline, package registry, plugin compatibility service, or formal support program.

## Version intent

The framework follows semantic versioning:

- **Patch:** Corrections and non-breaking improvements.
- **Minor:** Backward-compatible features and modules.
- **Major:** Breaking architectural or contract changes.

Pre-`1.0` releases communicate active design evolution; breaking changes still require explicit documentation, migration guidance, and review.

## Development model

The preferred future approach is trunk-based development:

- short-lived topic branches;
- pull requests into a protected default branch;
- required checks and reviews before merge;
- releasable default branch;
- release tags created from reviewed commits.

Temporary release branches may be used for supported security or maintenance lines when justified. Long-lived divergence is avoided.

## Pull request expectations

Each pull request identifies scope, linked requirement, risk, compatibility, affected contracts, validation, documentation, release-note impact, and required approvals. It follows the repository template and satisfies the [Definition of Done](../../standards/definition-of-done.md).

Architecture, governance, security, metadata-contract, precedence, and breaking changes require maintainer review and the applicable ADR or decision update. Authors do not provide the sole approval for high-impact changes.

## Required reviews

At minimum:

- a maintainer reviews framework behavior and consistency;
- content owners review affected standards or knowledge;
- security reviews security-boundary, plugin-execution, identity, access, or supply-chain changes;
- release authority confirms release evidence.

Organizations and future branch protections may impose stricter requirements.

## Changelog and release notes

Notable unreleased changes accumulate in [CHANGELOG.md](../../CHANGELOG.md) under `Unreleased`. At release, entries move to a dated version section. Release notes summarize outcomes, compatibility, migration, deprecations, known issues, security information, and acknowledgements without exposing sensitive details.

## Tags and artifact identity

Final releases use signed or otherwise protected semantic-version tags where supported, such as `v1.2.3`. Tags identify immutable reviewed commits. Future packaged artifacts should record source commit, version, integrity information, build inputs, and provenance.

## Compatibility

Compatibility covers:

- governance and precedence contracts;
- metadata and document schemas;
- identifiers and links;
- agent, workflow, adapter, and plugin contracts;
- tooling input and output when tooling exists.

Every release states supported compatibility and known breaks. A compatible parser should ignore optional unknown fields where safe, but must reject unsupported required contracts.

## Deprecation and breaking changes

Deprecation identifies the affected contract, reason, replacement, migration, support window, and earliest removal version. Breaking changes require a major release once the framework reaches `1.0`, an ADR when architectural, and explicit human approval. Security necessity may shorten a deprecation period with documented rationale.

## Security releases

Security issues follow coordinated disclosure and the repository's future security policy. Releases minimize disclosure before a fix, identify affected versions, provide remediation, preserve provenance, and may maintain supported patch lines. Compromised artifacts or plugins are revoked or withdrawn when possible.

## Documentation releases

Documentation is a versioned product artifact. Material guidance changes follow the same review, compatibility, changelog, and provenance expectations as executable contracts. Editorial-only corrections may be patch releases.

## Plugin compatibility

The future plugin model will declare compatible framework ranges. Framework releases must identify plugin-contract changes; plugin owners validate their own versions. No plugin compatibility automation currently exists, and framework compatibility does not imply enterprise approval.

## Rollback and recovery

Before release, maintainers identify how to revert the default branch, withdraw artifacts, revoke compromised versions, restore documentation, and communicate impact. Data migrations are not currently part of the framework; any future stateful service requires separately approved recovery design.

## Support policy

A formal support window is planned before `1.0`. Until approved, the project should support the current development line on a best-effort basis and prioritize critical security corrections. No service-level commitment is implied.

## Release evidence

The release record should include:

- version, commit, tag, and contents;
- approvals and responsible release authority;
- change and compatibility summary;
- link and metadata validation;
- tests and conformance checks available at that time;
- security review and dependency or supply-chain evidence;
- deprecations, migrations, known issues, and residual risks;
- artifact provenance and integrity;
- rollback and communication plan.

An agent may assemble evidence and recommend readiness but cannot authorize its own release.

## Related documents

- [Execution Model](EXECUTION_MODEL.md)
- [Security Model](SECURITY_MODEL.md)
- [Plugin Model](PLUGIN_MODEL.md)
- [Roadmap](../../ROADMAP.md)
