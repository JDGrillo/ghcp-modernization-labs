# Lab 8: Implementation readiness and early quality gates

**Modernization outcome:** A learner-reviewed execution and validation strategy for the
approved slice  
**Copilot concepts:** Evidence levels, stop-the-line gates, and cheapest falsifying checks

**Prerequisite:** Lab 7's `to-implementation` transition passes for exactly one
approved backend/target pair. The selected implementation toolchain need not be used
until its availability check later in this lab.

## Learn

The implementation handoff is not permission to generate the whole stack and inspect it
at the end. Before coding, establish what each component must prove, which command will
prove it, what remains unproven, and where the agent must stop for learner review.

This is a read-only review of the approved plan. Keep the deliverable in chat: do not
edit approved planning artifacts, create an implementation report, create `target/`,
or run implementation commands. A deficient gate strategy returns to planning for a
new revision and human approval; it is not patched after approval in this lab.

## Exercise

1. Read the shared [implementation quality gates](../IMPLEMENTATION-GATES.md).
2. Review the approved slice’s rule, interface, task, oracle, security, transaction,
   accessibility, database, operational, and rollback requirements.
3. Select the matching specialist from the approved lifecycle values:
   - **Java Implementation Agent** for `java-spring`;
   - **Dotnet Implementation Agent** for `dotnet-aspnet-core`.
4. Ask that agent to propose, without editing files:
   - the domain, backend/API, database, frontend, local integrated, Azure, and
     independent validation gates required by this slice;
   - stable check IDs and their mapped rule/interface/task/oracle IDs;
   - the cheapest falsifying check after each planned edit;
   - the exact evidence each gate will record and what it cannot prove;
   - which unavailable environments or dependencies must be marked blocked.
5. Critique the proposal. Reject any gate based only on generated code, compilation,
   mocks, snapshots, health checks, port checks, or local SQL when a stronger claim is
   being made.
6. Confirm the selected toolchain and local SQL prerequisites from Lab 0 are available:
   an approved LTS JDK and wrapper for Java, or an approved .NET LTS SDK pinned by
   `global.json` for .NET, plus the approved Node.js/package-manager baseline. Check
   Docker only when the later local SQL gate uses the containerized SQL Server profile.
   “Latest” means the current organization-supported stable release, never an
   unreviewed preview.
7. Capture the reviewed proposal in the same chat using this minimum table:

   | Check ID | Layer | Approved IDs exercised | Planned command/environment | Assertion | Evidence to record | Does not prove | Stop/review point |
   |---|---|---|---|---|---|---|---|

   Use the stable check IDs from the approved plan; do not invent new scope. Mark an
   unavailable dependency `blocked`, not passed or implicitly deferred. Lab 9 uses this
   reviewed chat output to initialize the application-scoped implementation report;
   product code alone goes under the selected target root. Neither action changes the
   approved plan revision.

## Verify

- Every in-scope rule and interface maps to at least one planned executable check.
- Each component has an explicit stop point and learner review.
- Database proof includes a clean migration, real SQL integration, and persisted state.
- Frontend proof includes behavior, contract handling, keyboard flow, and accessibility.
- Full-stack proof starts real components and drives browser-to-database cases.
- Azure compatibility and independent parity remain distinct from local success.
- A repair to an earlier component requires rerunning affected downstream gates.
- The selected agent, path instructions, target root, reports, and commands all match
  `activeSlice.backendPlatform`; the unused framework tree is not created.
- `git status --short` shows no changes caused by Lab 8 and `target/` remains absent for
  a fresh run.

## Explain

Why is a green build useful but insufficient? Why should the agent run a focused rule
test before a full-stack E2E suite? Who decides whether blocked evidence can be accepted?

**Exit criterion:** The learner can identify the earliest gate that would catch each
likely defect, the reviewed table is available in chat, required Lab 9 toolchain checks
pass, and no approved artifact or target code changed.

Continue to [Lab 9](../09-implementation-kickoff/README.md).