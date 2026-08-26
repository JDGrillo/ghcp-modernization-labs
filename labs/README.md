# GitHub Copilot mainframe modernization labs

These labs teach GitHub Copilot customization primitives by using them to modernize
one evidenced COBOL capability. The repository contains the completed customization
system; learners deconstruct it, exercise it, and explain why each primitive exists
before using the orchestrator.

Start with Lab 0 to understand the repository and verify prerequisites. Use `SURVDEMO`
for Labs 1-16 so participants can compare observations. Lab 17 uses `BANKDEMO` or
`TRSYDEMO` as a transfer exercise.

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
| 9 | Framework-specific implementation agent | Bind approved rules to Java or C# domain tests |
| 10 | Backend path instructions and API gate | Prove the selected backend and HTTP behavior |
| 11 | Database instructions and integration gate | Run migrations, backend, and real SQL persistence |
| 12 | Frontend instructions and component gate | Prove React contract handling and accessibility |
| 13 | E2E tools and local integrated gate | Run browser-to-database oracle cases |
| 14 | Independent validation agent | Produce a revision-bound gate verdict |
| 15 | Deployment agent, skill, and path instructions | Produce a private, identity-based Terraform plan |
| 16 | Approval gate and critic handoff | Apply one reviewed plan and independently validate Azure |
| 17 | Orchestrator agent | Route a second application to its correct stage |

Labs 1-5 form the customization workshop. Labs 6-7 require the lifecycle prerequisites
from Lab 0. Labs 8-14 require the selected development toolchain, Labs 15-16 add the
Azure/Terraform prerequisites, and Lab 17 transfers the lifecycle reasoning to a second
application. Labs 8-16 use the shared [implementation and deployment quality
gates](IMPLEMENTATION-GATES.md) to stop incorrect work at the earliest responsible
layer.

Read [Backend framework options](FRAMEWORK-OPTIONS.md) before approving the slice in
Lab 7. It explains the Java/.NET choice, agent routing, version policy, and review
criteria used through the rest of the practicum.

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
lifecycle checkpoints.

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