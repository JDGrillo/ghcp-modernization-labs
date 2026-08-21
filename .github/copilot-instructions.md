# Mainframe modernization policy

This repository incrementally replaces evidenced mainframe capabilities with React, Azure SQL Database, and one approved backend: Java with Spring Boot or .NET with ASP.NET Core. Correctness, traceability, security, and operational continuity take precedence over speed or code volume.

- Treat `legacy-source/` as immutable forensic evidence. Never edit, format, rename, move, regenerate, or repair it in place.
- Separate observed facts, interpretations, assumptions, and unresolved gaps. Never invent missing copybooks, layouts, schemas, contracts, mappings, side effects, or failure behavior.
- Recover and implement one bounded business capability at a time. Each slice must name its entry points, exclusions, rule IDs, interfaces, data, oracle cases, acceptance gates, and rollback.
- Maintain `modernization/<application-id>/lifecycle.json` and the canonical artifact indexes defined under `.github/templates/modernization/`; use them as the source of lifecycle stage, status, revisions, and handoff paths.
- Agents may prepare work for review but must never record their own approval. Only an accountable human or external approval process may set an approval decision to approved.
- Give every recovered rule a stable ID, precise legacy evidence citation, target mapping, and at least one test. Target-derived tests are not independent parity evidence.
- Preserve externally observable precision, rounding, encoding, fixed-width behavior, null versus blank, ordering, transactions, restart, return codes, authorization, audit, and side effects unless an approved requirement changes them.
- Before implementation, require a lifecycle-bound source-to-target map, aggregate data profile, migration runbook, reconciliation plan with predeclared tolerances, and rehearsed rollback or forward-recovery plan. Never treat successful DDL execution as proof that migrated data is complete or correct.
- Put discovery and planning evidence under `modernization/`. Put target code only under the approved `activeSlice.targetRoot`: `target/react-spring-azure-sql/` or `target/react-dotnet-azure-sql/`. Do not mix both backends in one slice or introduce another stack.
- Keep React presentation, backend application/domain behavior, and data/integration adapters separate. The selected backend owns authoritative business rules and transactions; the browser communicates through approved framework-neutral contracts only.
- Record `activeSlice.backendPlatform` and `activeSlice.targetRoot` during planning. Changing frameworks requires a revised plan and human approval, not an implementation-time substitution.
- Target Azure SQL Database. Local SQL Server is an inner-loop test environment, not Azure compatibility evidence.
- Provision Azure with reviewed Terraform only; never use `azd`. Require protected remote state, private data-plane connectivity, a WAF-controlled edge, managed workload identities, Microsoft Entra user and database authentication, federated CI/CD identity, least privilege, diagnostics, policy checks, and approval bound to a saved-plan digest.
- Validate trust boundaries, use parameterized data access and least privilege, redact protected data, and never place credentials or production records in source, prompts, fixtures, snapshots, or logs.
- Stop schema or data migration on unmapped fields, silent truncation/coercion, checksum drift, unowned rejects, reconciliation tolerance breach, or a destructive change without approved recovery evidence.
- Pin approved dependencies and record consequential contract, schema, infrastructure, security, and operational decisions.
- Keep changes reviewable and reversible. Update traceability, tests, risks, and runbooks with the implementation.
- Report commands and actual pass, fail, skip, and blocked results. Never claim parity, readiness, or completion while critical evidence, approvals, or validation gates are missing.

Use the role-based agents in `.github/agents/` for discovery, planning, implementation, independent validation, and approval-controlled Azure deployment. Use path-scoped instructions for technology-specific rules and skills for repeatable specialist procedures.
