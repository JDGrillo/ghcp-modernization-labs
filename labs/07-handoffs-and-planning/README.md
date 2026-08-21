# Lab 7: Handoffs, human gates, and planning

**Modernization outcome:** One approved, bounded vertical-slice plan  
**Copilot primitives:** Agent handoff and deterministic lifecycle gate

## Prerequisites

- Lab 6 produced a reviewable `APP-SURVDEMO` discovery package.
- Discovery is not blocked and critical gaps are empty.
- An accountable reviewer is available to approve discovery and, separately, the plan.
- Read [Backend framework options](../FRAMEWORK-OPTIONS.md) before selecting a backend.

## Learn

A handoff starts a new specialist context with explicit artifact identities. It does
not make an approval decision. The lifecycle manifest and validator prevent polished
prose or conversational references such as “this plan” from becoming authority.

## Exercise A: Approve discovery

1. Review the discovery index, critical gaps, evidence coverage, and source revision.
2. Do not approve if a critical gap can change the proposed modernization behavior.
3. As the accountable lab reviewer, update the lifecycle manifest:
   - set `status` to `approved`;
   - set `approval.decision` to `approved`;
   - record your name, timestamp, and a durable lab review reference.
4. Run:

   ```powershell
   python -B .github/scripts/validate_lifecycle.py `
     modernization/APP-SURVDEMO/lifecycle.json `
     --transition to-planning
   ```

5. Intentionally change one revision in a copy of the manifest or index, observe the
   failure, then discard the copy. Do not corrupt approved evidence.

## Exercise B: Plan the slice

1. Use the Legacy Analyst’s **Plan the first MVP** handoff.
2. Confirm the handoff states the manifest path, application ID, source revision,
   discovery-index path, approval decision, and critical-gap count.
3. Let the Modernization Planner select the smallest useful evidence-ready slice.
4. Inspect its agent and skill while it works. Identify what belongs to planning rather
   than discovery or implementation.
5. Review the generated slice-plan index, contracts, traceability, gates, exclusions,
   rollback, and decision owners. For data in scope, require the canonical field map,
   aggregate profile, migration runbook, reconciliation plan with tolerances, and
   recovery runbook before approving implementation.
6. Compare the two supported backend choices before approval:

   | Choice | Lifecycle values | Inspect |
   |---|---|---|
   | Java | `java-spring`, `target/react-spring-azure-sql` | LTS JDK/Spring support, team skills, Spring Batch/data-access fit, operations, dependencies |
   | .NET | `dotnet-aspnet-core`, `target/react-dotnet-azure-sql` | .NET LTS/ASP.NET Core support, team skills, hosted/background processing and data-access fit, operations, dependencies |

   Require an ADR covering support lifecycle, enterprise standards, skills, hosting,
   identity, batch/restart semantics, transaction needs, licensing, cost, and delivery
   risk. “The agent chose it” is not a rationale.
7. Select exactly one pair in `activeSlice.backendPlatform` and `targetRoot`. Confirm
   contracts and oracle outcomes remain framework-neutral.
8. Confirm the planner reset approval to pending and left planning ready for review.
9. After human review, record planning approval in the lifecycle manifest and run:

   ```powershell
   python -B .github/scripts/validate_lifecycle.py `
     modernization/APP-SURVDEMO/lifecycle.json `
     --transition to-implementation
   ```

## Verify

The validator checks application, source, slice, plan, contract, and oracle-set
identities as well as required files and critical gaps. The approved slice names
explicit exclusions, rollback, backend platform, target root, and enforceable data
migration controls; it is not merely a list of technical tasks.

## Explain

Why are handoffs, lifecycle manifests, and validators three separate mechanisms? Which
one carries context, records state, and enforces transition prerequisites?

**Exit criterion:** `to-implementation` passes for exactly one human-approved slice and
one matching backend/target pair.

Continue to [Lab 8](../08-implementation-readiness/README.md).