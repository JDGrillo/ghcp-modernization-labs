---
name: implement-mainframe-slice
description: "Implement one approved mainframe modernization slice using React, Azure SQL, and its selected Java/Spring Boot or .NET/ASP.NET Core backend. Use for domain rules, APIs, persistence, tests, traceability, and repair."
user-invocable: false
---

# Implement Mainframe Slice

Build one approved vertical slice without changing its evidence or scope.

## Entry gate

Require `modernization/<application-id>/lifecycle.json` and run `python -B .github/scripts/validate_lifecycle.py <manifest> --transition to-implementation`. Do not proceed unless it passes. Bind implementation to the manifest's application ID, source revision, active slice and revisions, `backendPlatform`, `targetRoot`, slice-plan index, traceability index, and approved artifact paths. Refuse to write outside the selected target root.

## Procedure

1. Create the reproducible target skeleton and a draft implementation report. Bind approved characterization values into exact domain tests.
2. Implement framework-independent domain types and rules in the selected language. Use Java `BigDecimal` or C# `decimal` with explicit precision, scale, rounding, comparison, and overflow behavior. Pass and record the domain gate before continuing.
3. Implement application orchestration, authorization, idempotency, concurrency, transaction intent, the approved OpenAPI operation, and safe errors behind persistence ports. Pass and record the backend/API component gate before continuing.
4. Verify the approved data-migration artifacts, then add Azure SQL-compatible, versioned migrations and parameterized persistence adapters. Keep one migration chain, disable automatic production DDL, and use a clean real SQL Server for integration tests. Exercise clean install, supported upgrades, restart/repeat behavior, metadata, representative transformed data, rejects, reconciliation, and recovery. Pass and record the database gate, including a DB-touching API call and persisted-state assertion, before continuing.
5. Generate or validate TypeScript API types and implement the accessible React task. Do not duplicate authoritative rules in the browser. Pass and record the frontend typecheck, component, contract, keyboard, and accessibility gate before continuing.
6. Start the real local database, selected backend, and React frontend. Run approved browser-to-database cases and verify visible results, HTTP outcomes, database post-state, audit/correlation, and relevant side effects. Pass and record the local integrated gate before handoff.
7. Run Azure SQL compatibility, security, performance, resilience, restart, and operational gates required by the approved plan. Mark unavailable evidence blocked or skipped; never infer a pass from local results.
8. After each substantive edit, run the cheapest check that can falsify it. Do not proceed while the current component gate is failed or blocked. When an earlier component changes, rerun it and every affected downstream gate.
9. Update traceability, target README, runbooks, risks, and rollback notes throughout implementation rather than deferring them to the end.
10. Finalize an implementation report containing changed components and, for every check, its stable ID, layer, mapped rule/interface/task/oracle IDs, exact command, environment, exit code, result, behavioral assertion, artifact path, and evidence limit.
11. Update the lifecycle manifest to implementation and `implemented`, record the report and exact target revision, preserve all input revision identifiers, and run the `to-validation` gate.
12. Hand the result to an independent Validation Critic. Do not self-certify parity or readiness.

## Technical safeguards

- React communicates only through approved contracts and never accesses Azure SQL directly.
- Use the current organization-supported LTS runtime and a supported framework release, then pin the SDK/runtime and dependencies for reproducibility. “Latest” never means an unreviewed preview.
- Preserve exact decimal, date/time, fixed-character, null/blank, ordering, version, transaction, restart, and return-code behavior.
- Map Db2 `TIMESTAMP` date/time values to reviewed `datetime2` semantics, never SQL Server `timestamp`/`rowversion`.
- Local SQL Server is an inner-loop environment; it is not Azure SQL compatibility evidence.
- Never silently truncate, coerce, default, discard, or repair source values. Quarantine rejects with stable non-sensitive references and stop when approved tolerances are exceeded.
- Use expand/contract sequencing for destructive changes. A down migration is not recovery evidence unless it preserves accepted transactions and passes reconciliation after rehearsal.
- Unexpected failures must preserve the public error contract and retain diagnosable server-side cause and correlation data.
- A generated test, mock, snapshot, health endpoint, port check, or successful compile proves only its own layer. Do not use one as a substitute for real database, browser-to-database, differential, Azure, or readiness evidence.

Use the implementation references when needed: [React](./references/react-frontend.md), [Spring and Azure SQL](./references/spring-azure-sql.md), [.NET and Azure SQL](./references/dotnet-azure-sql.md), and [local SQL testing](./references/local-sql-testing.md).
