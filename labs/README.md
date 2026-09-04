# GitHub Copilot mainframe modernization labs

These labs teach GitHub Copilot customization primitives by using them to modernize
one evidenced COBOL capability. The repository contains the completed customization
system; learners deconstruct it, exercise it, and explain why each primitive exists
before using the orchestrator.

Start with Lab 0 to understand the repository and verify prerequisites. Use `SURVDEMO`
for Labs 1-16 so participants can compare observations. Lab 17 uses `BANKDEMO` or
`TRSYDEMO` as a transfer exercise.

Lab numbers include Lab 0. Therefore, the first ten numbered labs are Labs 0-9;
Lab 10 begins backend/API implementation. Labs are cumulative: do not skip a lifecycle
gate or recreate artifacts that an earlier lab requires you to preserve.

## Learning path

| Lab | GitHub Copilot primitive | Modernization outcome |
|---|---|---|
| 0 | Workspace orientation | Understand the repository, prerequisites, and safe starting state |
| 1 | Chat context and effective requests | Define the application evidence boundary |
| 2 | Repository instructions | Identify always-on modernization policy |
| 3 | Path-specific instructions | Apply rules only where they are relevant |
| 4 | Hooks | Enforce immutable legacy evidence |
| 5 | Skills and bundled resources | Understand the reusable discovery procedure |
| 6 | Custom agents | Trace one entry point, then produce a bounded discovery package |
| 7 | Handoffs and lifecycle gates | Compare Java and .NET, then approve one slice and backend |
| 8 | Quality-gate strategy | Route to the matching agent and define early checks |
| 9 | Framework-specific implementation kickoff | Create the selected target skeleton and bind approved rules to Java or C# domain tests |
| 10 | Backend path instructions and API gate | Prove the selected backend and HTTP behavior |
| 11 | Database instructions and integration gate | Run migrations, backend, and real SQL persistence |
| 12 | Frontend instructions and component gate | Prove React contract handling and accessibility |
| 13 | E2E tools and local integrated gate | Run browser-to-database oracle cases |
| 14 | Independent validation agent | Produce a revision-bound gate verdict |
| 15 | Deployment agent, skill, and path instructions | Produce a private, identity-based Terraform plan |
| 16 | Approval gate and critic handoff | Apply one reviewed plan and independently validate Azure |
| 17 | Orchestrator agent | Route a second application to its correct stage |

Labs 1-5 form the customization workshop. Labs 6-7 require the lifecycle prerequisites
from Lab 0. Lab 8 verifies the selected development toolchain without generating code;
Labs 9-14 use it. Labs 15-16 add the Azure/Terraform prerequisites, and Lab 17
transfers the lifecycle reasoning to a second application. Labs 8-16 use the shared [implementation and deployment quality
gates](IMPLEMENTATION-GATES.md) to stop incorrect work at the earliest responsible
layer.

Read [Backend framework options](FRAMEWORK-OPTIONS.md) before approving the slice in
Lab 7. It explains the Java/.NET choice, agent routing, version policy, and review
criteria used through the rest of the practicum.

## Sequencing and preserved state

| Phase | Hard entry condition | State to preserve |
|---|---|---|
| Labs 0-5 | Open the repository root in a Git worktree; Python checks pass | Chat notes and actual command results; no generated lifecycle artifacts |
| Lab 6 | Labs 1-5 complete; clean-run `modernization/` contains only its contract README | The application-scoped discovery package |
| Lab 7 | Discovery is reviewable, critical gaps are empty, and an accountable reviewer is available | Discovery approval, then the separately reviewed slice plan and planning approval |
| Lab 8 | `to-implementation` passes for one approved backend/target pair | A chat-only implementation gate review; do not revise approved planning artifacts |
| Lab 9 | Lab 8 review is complete and the selected development toolchain is available | Selected target root, draft implementation report, traceability, and domain-gate evidence |
| Lab 10 | The Lab 9 domain gate passes and is recorded | All Lab 9 state plus the backend/API component and its gate evidence |

A **Verify** check in Labs 0-8 confirms that a response, customization behavior, or
lifecycle artifact has the expected shape and authority. A **Gate** in Labs 9-16 is a
stop-the-line executable check: failure or blocked evidence prevents work from moving
to the next component. Human approval remains separate from both.

## Lab method

The sequence repeatedly uses five learning actions:

1. **Orient** to the named repository artifacts, their purpose, and their expected effect.
2. **Inspect** the customization file and its activation mechanism.
3. **Demonstrate** the primitive with a provided prompt or command against real evidence.
4. **Verify** an observable response, artifact, command result, or denied action.
5. **Explain** why a neighboring primitive would not solve the same problem.

Lab 0 establishes orientation and readiness. Labs 1-8 label the observable checks as
**Verify**; implementation and deployment Labs 9-16 make those checks stricter under
**Gate**; Lab 17 returns to **Verify** for the transfer exercise. Each lab identifies
the important artifacts and expected behavior before asking the learner to demonstrate
or verify them.

Do not modify `legacy-source/`. Preserve generated `modernization/` artifacts from Lab
6 onward and `target/` artifacts from Lab 9 onward because they are cumulative
lifecycle checkpoints. To repeat a stage, first preserve the current run on a branch,
tag, commit, or separate lab copy; never delete approved evidence in place.

## Completion standard

A learner completes the series when they can:

- distinguish instructions, path instructions, skills, agents, handoffs, and hooks;
- explain when separate Java/.NET agents are preferable to one conditional agent and
    route from lifecycle state rather than conversational preference;
- identify from repository configuration when each primitive is loaded or invoked;
- trace a recovered rule from immutable evidence through plan, code, test, and validation;
- distinguish domain, API, database, frontend, local integrated, Azure compatibility,
    parity, Terraform plan/apply, Azure validation, and readiness evidence;
- explain why approval and lifecycle transitions are machine-checkable;
- use the orchestrator without treating it as a black box.

Begin with [Lab 0](00-orientation/README.md).