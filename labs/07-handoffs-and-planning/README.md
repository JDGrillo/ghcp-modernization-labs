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

This lab has two separate human decisions. Discovery approval establishes that the
evidence is sufficient to plan; planning approval authorizes one bounded slice and one
backend/target pair for implementation. The manifest's single `approval` object is
stage-scoped: the planner must reset it to pending when moving from discovery to
planning, so discovery approval cannot silently authorize implementation.

## Exercise A: Discovery approval gate

1. Confirm the manifest is at `currentStage: discovery`, has status
   `ready-for-review`, leaves `approval.decision` pending, and references the source
   revision and canonical discovery index you reviewed.
2. Review every indexed artifact, the automated-analysis reconciliation, evidence
   coverage, and critical gaps. Do not approve if an unresolved gap can change an
   in-scope business rule, field mapping, interface outcome, transaction/failure
   behavior, authorization boundary, or independent oracle.
3. As the accountable lab reviewer, update the lifecycle manifest:
   - set `status` to `approved`;
   - set `approval.decision` to `approved`;
   - record your name in `approvedBy`, an RFC 3339 timestamp in `approvedAt`, and a
     durable review identifier or URL in `decisionReference`.
4. Run:

   ```powershell
   python -B .github/scripts/validate_lifecycle.py `
     modernization/APP-SURVDEMO/lifecycle.json `
     --transition to-planning
   ```

5. Copy `lifecycle.json` to an untracked
   `modernization/APP-SURVDEMO/lifecycle.negative-test.json`. Change only the
   `sourceRevision` in that copy, run `to-planning` against the copied manifest, and
   observe that its revision no longer matches the referenced discovery index. Remove
   the copy and confirm `git status --short` shows no change to the reviewed evidence.

## Exercise B: Planning approval gate

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
8. Before planning approval, confirm the planner set `currentStage` to `planning`,
   left status `ready-for-review`, and reset every approval field: decision is pending
   and `approvedBy`, `approvedAt`, and `decisionReference` do not carry the discovery
   approval forward. Verify that the manifest and slice-plan index agree on application,
   source, slice, plan, contract, oracle-set, backend, and target-root identities.
9. Review the complete planning package. Reject it if data movement is in scope but a
   field map, aggregate profile, immutable snapshot reference, migration/reconciliation
   controls, reject handling, or recovery mode is missing. If data movement is out of
   scope, require its reason and approved decision path.
10. As the accountable reviewer, set planning status and approval to `approved`, record
   new stage-specific reviewer metadata, then run:

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

Record both command outcomes: `to-planning` passes only after discovery approval, and
`to-implementation` passes only after the separate planning approval. A handoff button,
agent response, or previous-stage approval is not equivalent to either result.

## Explain

Why are handoffs, lifecycle manifests, and validators three separate mechanisms? Which
one carries context, records state, and enforces transition prerequisites?

**Exit criterion:** `to-implementation` passes for exactly one human-approved slice and
one matching backend/target pair.

Lab 8 reviews how that approved slice will be checked; it does not modify the approved
plan or begin implementation.

Continue to [Lab 8](../08-implementation-readiness/README.md).