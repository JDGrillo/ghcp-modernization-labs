# Lab 8: Implementation readiness and early quality gates

**Modernization outcome:** A learner-reviewed execution and validation strategy for the
approved slice  
**Copilot concepts:** Evidence levels, stop-the-line gates, and cheapest falsifying checks

## Learn

The implementation handoff is not permission to generate the whole stack and inspect it
at the end. Before coding, establish what each component must prove, which command will
prove it, what remains unproven, and where the agent must stop for learner review.

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
   `global.json` for .NET. “Latest” means the current organization-supported stable
   release, never an unreviewed preview.
7. Preserve the reviewed gate plan with the approved slice artifacts or implementation
   report draft before beginning target code.

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

## Explain

Why is a green build useful but insufficient? Why should the agent run a focused rule
test before a full-stack E2E suite? Who decides whether blocked evidence can be accepted?

**Exit criterion:** The learner can identify the earliest gate that would catch each
likely defect and is ready to supervise component-by-component implementation.

Continue to [Lab 9](../09-implementation-kickoff/README.md).