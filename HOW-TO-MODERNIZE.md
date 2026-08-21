# How to modernize with GitHub Copilot

This repository uses role-based GitHub Copilot agents, focused skills, path instructions, and one deterministic hook to modernize one evidenced business capability at a time.

## Customization model

| Primitive | Purpose in this repository |
|---|---|
| Repository instructions | Non-negotiable evidence, traceability, security, and lifecycle policy |
| Path instructions | Rules for legacy evidence, modernization artifacts, frontend, backend, database, local SQL, E2E, or Terraform infrastructure files |
| Custom agents | Separate responsibilities, tools, context, and lifecycle authority |
| Skills | Repeatable specialist procedures loaded by the relevant agent |
| Handoffs | Explicit transitions from discovery through validation, deployment, and Azure validation |
| Hooks | Deterministic enforcement that instructions alone cannot guarantee |

Select a specialist agent directly or use the Modernization Orchestrator after learning the stages. The Legacy Analyst supports chat-only reconnaissance for one named entry point as well as full skill-driven discovery.

## Clean starting state

Before a test run, `modernization/` should contain only its contract README and `target/` may be absent. Discovery creates the evidence baseline. Planning selects `java-spring` with `target/react-spring-azure-sql` or `dotnet-aspnet-core` with `target/react-dotnet-azure-sql`. Implementation creates only that target root and records its exact revision. Validation and deployment artifacts retain the platform identity.

Commit or otherwise preserve a completed run before resetting these directories. They contain traceability and approval evidence, not disposable build output.

## 1. Discover and document

Select **Legacy Analyst** and identify an application boundary:

```text
Analyze SURVDEMO as immutable legacy evidence. Recover and document its entry
points, dependencies, business rules, data semantics, user tasks, transactions,
failure and restart behavior, interfaces, characterization coverage, and risks.
Refresh the project documentation from approved evidence. Do not design or
implement target code.
```

The analyst uses `discover-mainframe-application`. Expected outputs include `modernization/<application-id>/lifecycle.json`, a canonical discovery index, system context, entry-point inventory, dependency graph, business-rule catalog, data dictionary, transaction and failure model, characterization index, and risk register.

Discovery is blocked only where missing or conflicting evidence can change the result. A polished README does not replace the underlying evidence artifacts.

The analyst leaves discovery `ready-for-review`. After an accountable human records approval, verify the handoff with `validate_lifecycle.py --transition to-planning`.

## 2. Plan the MVP and roadmap

Use the analyst's **Plan the first MVP** handoff or select **Modernization Planner**:

```text
Using the approved SURVDEMO discovery evidence, plan the smallest useful
end-to-end MVP in React, Azure SQL, and the enterprise-approved Java/Spring Boot or
.NET/ASP.NET Core backend. Define later slices for the
remaining behavior. Do not modify legacy evidence or target code.
```

The planner uses `plan-mainframe-modernization` and must define:

- a useful business capability, actors, entry points, and exclusions;
- rule, interface, data, and independent oracle IDs;
- a framework-selection ADR, `backendPlatform`, `targetRoot`, React tasks and states,
  framework-neutral OpenAPI/errors, backend use cases, and Azure SQL mappings;
- a lifecycle-bound source-to-target map, aggregate profile, migration/reconciliation
    runbooks with predeclared tolerances, reject handling, and rollback or forward recovery;
- authorization, transactions, concurrency, restart, audit, and operational requirements;
- planned tests, measurable acceptance gates, rollback, risks, decisions, and owners;
- a dependency-ordered roadmap for later online, batch, integration, and cutover slices.

Implementation does not begin until critical contracts and evidence gaps are resolved or explicitly approved by accountable owners.

The planner leaves the selected slice `ready-for-review` in the lifecycle manifest. After human approval, verify the explicit application, source, slice, plan, contract, oracle-set, and artifact references with `validate_lifecycle.py --transition to-implementation`.

## 3. Implement one approved slice

Use the planner handoff matching the lifecycle: **Implement with Java and Spring Boot**
or **Implement with .NET and ASP.NET Core**.

Both implementation agents use `implement-mainframe-slice` and the path instructions
for their selected target root. They work in this order:

1. Bind approved characterization outcomes into exact tests.
2. Implement framework-independent Java or C# domain rules.
3. Add application orchestration, authorization, concurrency, and transactions.
4. Add reviewed Azure SQL migrations and parameterized persistence; prove clean and
    supported upgrades, restart/replay, mapped data load, rejects, reconciliation, and
    recovery against one immutable source snapshot.
5. Implement the approved API and safe error behavior.
6. Implement the accessible React task from the approved contract.
7. Add the required focused and integrated tests.
8. Update traceability, target documentation, runbooks, risks, and rollback notes.

After each substantive edit, run the cheapest check capable of falsifying it. Do not broaden the slice to resolve unrelated behavior.

Before validation, the selected agent records the implementation report, platform/root,
and `activeSlice.targetRevision`; `validate_lifecycle.py --transition to-validation` must pass.

## 4. Validate independently

Use the selected implementation agent's **Run independent validation** handoff or select **Validation Critic**.

The critic has read, search, execute, and evidence-writing tools. Its edit authority is limited to new validation findings and gate reports; it cannot modify product code, tests, plans, or approved evidence. It uses `validate-mainframe-modernization` to:

- verify bidirectional rule and interface traceability;
- criticize target-derived tests, weak assertions, mocks, and missing boundaries;
- run applicable domain, API, frontend, accessibility, database, E2E, security, concurrency, performance, restart, and resilience checks;
- compare target outputs and persisted state with approved legacy outcomes;
- classify every gate as passed, failed, skipped, or blocked;
- report findings by severity and give the narrowest evidence-supported verdict.

The critic does not fix its own findings. Repairs return to the same lifecycle-selected implementation agent and are independently revalidated.

The critic writes a canonical validation gate report tied to all input revisions. A
`passed` verdict may proceed to the next slice or to enterprise deployment planning.

## 5. Plan and deploy to Azure

Use the critic's **Prepare an Azure deployment plan** handoff or select **Azure
Deployment Agent**. It uses `deploy-enterprise-azure-slice`; it must retrieve current
Azure and Terraform guidance and must never invoke `azd`.

Run `validate_lifecycle.py --transition to-deployment-plan`. Record an architecture
decision for the exact environment before generating Terraform. The default control
set is a WAF HTTPS edge; private application origins, registry, Key Vault, and Azure
SQL; private DNS and explicit egress; managed runtime identities; Microsoft Entra user
and SQL authentication; workload identity federation for CI/CD; least-privilege RBAC;
diagnostics, alerts, policy, backup, and cost controls.

Run format, validate, lint, tests, security/policy scans, cost estimation, and plan.
Store a saved plan only as a protected short-lived artifact and record its SHA-256
digest. Bind the migration revision, protected source snapshot and pre-migration backup,
restore rehearsal, reconciliation tolerances, and recovery runbook. The agent leaves
deployment `planned` and approval pending.

After an accountable reviewer approves that digest and environment, run
`--transition to-deployment-apply`. Apply only the exact saved plan, without
`-auto-approve`, then record resource identities, state serial, migrations,
snapshot-bound reconciliation, rejects, connectivity, identity, diagnostics, and
recovery checks. Run
`--transition to-azure-validation` and hand off to the Validation Critic. Terraform
convergence, Azure compatibility, application behavior, production readiness, and
cutover authority remain separate claims.

## 6. Repeat or prepare cutover

After a slice passes its required gates, return to the roadmap and select the next dependency-ready capability. Coexistence, data migration, parallel run, reconciliation, rollback rehearsal, and decommissioning are planned and validated as explicit slices or readiness gates, not assumed from feature completion.

## Hook behavior

`.github/hooks/protect-legacy-source.json` runs before tool use. Its Python policy script allows dedicated read and search tools for `legacy-source/`, denies recognized file mutations, and conservatively denies terminal commands that reference the protected directory because shell text cannot be proven read-only.

The hook supplements, rather than replaces, source-control review and filesystem permissions. Run its focused regression suite with:

```powershell
python -B .github/hooks/test_protect_legacy_source.py -v
```

Use dedicated workspace tools rather than terminal commands to read protected evidence.

## Validation layers

| Layer | Evidence produced |
|---|---|
| Domain and unit | Exact recovered rule behavior and boundaries |
| API and contract | Transport validation, authorization, DTOs, and errors |
| Frontend and accessibility | User-task states, keyboard behavior, semantics, and announcements |
| Database integration | Real migration, SQL, mappings, constraints, and transactions |
| Full-stack E2E | Browser-to-API-to-database behavior |
| Differential parity | Target outcomes and persisted state compared with approved legacy outcomes |
| Terraform plan | Reviewed intended resources, exposure, grants, policy, cost, and destructive changes |
| Terraform apply | Convergence of the approved saved-plan digest in the named environment |
| Azure validation | Private connectivity, identity, Azure SQL, application, security, recovery, and operations |

Passing one layer does not imply another. Report exact commands and pass, fail, skip, and blocked results.

## Definition of done for a slice

- Every in-scope rule and interface has evidence, a target mapping, and a test.
- Approved oracle outcomes remain exact and unchanged.
- Contracts, migrations, seeds, queries, and generated clients agree.
- Precision, encoding, fixed-width, null/blank, ordering, transaction, failure, and restart behavior are verified where applicable.
- Security, accessibility, operations, reconciliation, and rollback gates have explicit results.
- Infrastructure has no unapproved public data plane, stored deployment credential, broad role, or unowned private DNS/federation dependency.
- Independent validation has no unresolved critical mismatch.
- The readiness claim uses only the narrowest status supported by evidence.
