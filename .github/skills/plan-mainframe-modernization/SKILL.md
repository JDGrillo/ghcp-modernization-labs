---
name: plan-mainframe-modernization
description: "Plan an incremental mainframe migration to React, Azure SQL, and either Java/Spring Boot or .NET/ASP.NET Core. Use for framework selection, slices, contracts, gates, coexistence, rollback, and cutover."
user-invocable: false
---

# Plan Mainframe Modernization

Turn approved discovery evidence into an incremental, testable delivery plan.

## Entry gate

Require `modernization/<application-id>/lifecycle.json` and run `python -B .github/scripts/validate_lifecycle.py <manifest> --transition to-planning`. Do not proceed unless it passes. Use the application ID, source revision, and discovery-index path from that manifest; do not convert unresolved behavior into a design assumption.

## Procedure

1. Inventory candidate user and batch capabilities with their business value, dependencies, risk, and evidence readiness.
2. Select the smallest useful end-to-end MVP that exercises a real entry point, meaningful business rules, backend behavior, and persistence where the capability requires it.
3. Define the MVP's actors, entry points, rules, interfaces, data, security, operations, exclusions, intentional changes, and dependencies.
4. Compare `java-spring` and `dotnet-aspnet-core` using documented enterprise criteria: supported runtime lifecycle, organization skills and standards, dependencies, batch/restart fit, transaction/data-access needs, hosting, identity, operations, licensing, delivery risk, and total cost. Record the decision in an ADR.
5. Set exactly one matching pair in the active slice: `java-spring` with `target/react-spring-azure-sql`, or `dotnet-aspnet-core` with `target/react-dotnet-azure-sql`. Keep OpenAPI and business semantics framework-neutral.
6. Map legacy tasks to React routes and states, public operations and errors to OpenAPI, domain behavior to selected-backend use cases, and legacy data to Azure SQL.
7. Profile sanitized source aggregates and complete the source-to-target map before DDL. Decide transaction, concurrency, idempotency, restart, audit, observability, migration/coexistence, reject handling, reconciliation tolerances, and rollback or forward-recovery behavior from evidence or explicit approved decisions.
8. Map each rule and interface to an oracle case, target component, planned test, and acceptance gate.
9. Sequence later slices by business value and dependency order to cover remaining online, batch, integration, operational, and cutover behavior.
10. Record decisions as ADRs, unresolved gaps as owned risks, and approvals as gates. Do not mark a gate approved on an agent's authority.
11. Copy and complete the canonical slice-plan index, update the lifecycle manifest to planning and `ready-for-review`, and leave approval pending for an accountable human.

## Required plan

Each slice must state:

- capability, actors, entry points, and exclusions;
- legacy artifacts, revision, rule IDs, interface IDs, and oracle IDs;
- framework decision, `backendPlatform`, `targetRoot`, and support assumptions;
- React, API, selected backend, Azure SQL, security, and operational mappings;
- dependencies and explicit non-goals;
- tests and measurable acceptance gates;
- data migration or coexistence needs;
- source snapshot identity, every source-to-target field mapping, profiling anomalies and owners, migration checkpoints, reject quarantine, predeclared reconciliation tolerances, and a rehearsable recovery mode;
- rollout, reconciliation, rollback, risks, decisions, and owners.

Write architecture and contracts under `modernization/<application-id>/architecture/`. Write each slice under `modernization/<application-id>/plans/<slice-id>/`, with canonical `slice-plan-index.json` and `traceability.json` files. Do not modify `legacy-source/` or `target/`.

Load [target architecture guidance](./references/target-architecture.md), [Azure SQL design guidance](./references/azure-sql.md), and [legacy UI recovery guidance](./references/legacy-ui-recovery.md) when those concerns are in scope.
