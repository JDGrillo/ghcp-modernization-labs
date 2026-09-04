# Lab 9: Implementation kickoff and domain rules

**Modernization outcome:** A reproducible target skeleton with approved rules bound to
framework-independent tests  
**Copilot primitive:** Edit-capable specialist agent constrained by a lifecycle gate

## Prerequisites

- `to-implementation` passes for exactly one approved slice.
- The repository is a clean Git worktree and approved evidence is preserved.
- Read the shared [implementation quality gates](../IMPLEMENTATION-GATES.md).
- The Lab 8 gate-review table is available in chat, and the selected runtime, build
   tool, Node.js/package manager, and any required local container prerequisite pass
   their version checks.

## Learn

The first implementation task is not to start three servers. It is to bind approved
characterization outcomes to the smallest executable domain tests. This catches rule,
precision, boundary, and interpretation errors before frameworks obscure them.

## Exercise

1. Inspect the selected Java or Dotnet Implementation Agent, its shared skill, and its
   framework-specific stack/backend instructions.
2. Use the planner handoff matching `activeSlice.backendPlatform`.
3. Confirm the agent states all lifecycle identities and runs `to-implementation`.
4. Give the agent this control instruction:

   ```text
   For Lab 9, implement only the reproducible target skeleton and approved domain
   rules. Run and record the domain gate, then stop for learner review. Do not begin
   the API, database, or frontend implementation in this run.
   ```

5. Require the agent to create only the selected target root and the minimum skeleton
   needed to build and test the domain layer: pinned runtime/build files, wrapper
   commands, safe environment examples, target README, domain source project/module,
   and domain test project/module. Do not scaffold API endpoints, persistence,
   migrations, frontend features, E2E tests, or infrastructure.
6. Initialize the implementation report from the canonical repository template at an
   application-scoped path under `modernization/`, then set
   `artifacts.implementationReport` in `lifecycle.json` to that path. Copy the approved
   lifecycle identities and the Lab 8 planned check IDs into it before running tests;
   record actual results rather than marking planned checks passed.
7. Implement only framework-independent domain types and rules needed by the slice.
8. Bind the characterization oracle inputs and expected outcomes approved in the Lab 7
   plan into exact tests, including
   boundaries, precision/rounding, null/blank, dates, codes, and error priority that
   apply to the slice.
9. After each rule edit, require the smallest relevant test. Then run the complete
   domain suite using the generated Maven/Gradle wrapper or `dotnet test` command.
10. Ask the agent to show one rule’s legacy citation, Java or C# implementation, test,
   actual command/result, and known limitation.
11. Leave `activeSlice.targetRevision` unset until the implementation evidence is
   captured in a stable repository revision. Do not use a dirty-worktree hash or label
   the partial Lab 9 component `implemented`; the complete implementation transition
   occurs only after the later component labs.

## Gate

Do not continue unless:

- the target build is reproducible from documented wrapper commands;
- dependency-free domain code has no Spring/ASP.NET Core, HTTP, ORM, or database imports;
- every in-scope domain rule has approved expected behavior and boundary coverage;
- exact decimal behavior uses Java `BigDecimal` or C# `decimal` with explicit scale,
  precision, rounding, comparison, and overflow semantics;
- the domain suite passes and its results are recorded in traceability;
- no target-derived expected result is presented as independent parity evidence;
- no API, persistence, migration, frontend feature, E2E, or infrastructure code was
   added as part of the skeleton.

**Exit criterion:** The domain gate passes; no API, migration, or UI claim is made yet.

Continue to [Lab 10](../10-backend-api/README.md).