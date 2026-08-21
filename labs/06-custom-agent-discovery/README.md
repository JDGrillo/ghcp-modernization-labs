# Lab 6: Custom agent, reconnaissance, and discovery

**Modernization outcome:** Trace one entry point, then produce a reviewable
`APP-SURVDEMO` discovery package  
**Copilot primitive:** Custom agent with role, tools, skill, boundaries, and handoff

## Prerequisites

- Labs 1-5 are complete.
- `modernization/` contains only its contract README for a clean run.
- The repository is under source control so the source revision can be recorded.

## Learn

An agent defines **who owns a stage**, which tools it can use, what context it should
isolate, and where its authority stops. The Legacy Analyst can perform a narrow,
chat-only reconnaissance request or load the discovery skill for a durable application
evidence package. It may not design or implement the target.

## Exercise A: Scoped reconnaissance

1. Inspect `.github/agents/legacy-analyst.agent.md`.
2. Predict what the agent may read, what it must not create during reconnaissance, and
   when the full discovery skill becomes necessary.
3. Select **Legacy Analyst** and submit:

   ```text
   Perform scoped reconnaissance only for SURVDEMO entry point SURVINQ in
   legacy-source/DEV1/SURVDEMO/COBOL/SURVINQ.cbl. Return a preliminary,
   chat-only evidence map with the exact entry-point citation, directly evidenced
   calls, copybooks, maps, transactions, tables, files, and interfaces; separate
   observed facts from interpretations; list blocking gaps and next files. Do not
   create modernization artifacts, infer the complete application boundary, plan
   target architecture, or propose target code.
   ```

4. Confirm that the response stays within the named entry point and creates no files.
5. Explain why the result is useful scoping evidence but not an approved discovery
   package or planning input.

## Exercise B: Full discovery

1. In a new Legacy Analyst chat, submit:

   ```text
   Analyze legacy-source/DEV1/SURVDEMO as application APP-SURVDEMO at the
   current immutable source revision. Use the full discovery skill and produce the
   required application-scoped evidence package and canonical indexes. Include the
   repository-native automated COBOL analysis as candidate evidence, preserve its
   coverage, diagnostics, and limitations, and create the required reconciliation
   record beside it. Treat source as immutable, separate analyzer-observed structures,
   analyst-confirmed facts, interpretations, and gaps, and stop before planning target
   code.
   ```

2. Let the agent complete discovery. Preserve blocked results rather than supplying an
   assumption when evidence is missing or conflicting.
3. Inspect `modernization/APP-SURVDEMO/evidence/automated-analysis/analysis.json` and
   `reconciliation.md`. Trace several candidate IDs to exact source coordinates, then
   locate their confirmed, rejected, or unresolved reconciliation decisions.
4. Inspect `modernization/APP-SURVDEMO/lifecycle.json` and the discovery index. Confirm
   that `automatedAnalysis` binds the analysis and reconciliation paths.
5. Follow several rule, interface, task, and oracle IDs into their detailed artifacts.
6. Run the transition validator. A draft or blocked discovery is expected to fail the
   approval gate; an approved review package must pass all evidence checks:

   ```powershell
   python -B .github/scripts/validate_lifecycle.py `
     modernization/APP-SURVDEMO/lifecycle.json `
     --transition to-planning
   ```

7. Ask the Legacy Analyst to implement one recovered rule. Confirm that it returns the
   work to the planning gate instead.

## Verify

- Reconnaissance produced no lifecycle or modernization artifact.
- Full discovery leaves stage `discovery` and status `ready-for-review` or `blocked`.
- Approval remains pending; the agent did not approve itself.
- Every discovery-index path exists.
- Automated analysis matches the application and source revision, has zero failed files
   and error diagnostics, records limitations, and has a separate reconciliation path.
- Partial analyzer coverage is not hidden; every warning is resolved or tracked as a gap.
- Conclusions cite immutable evidence and distinguish facts, interpretations, and gaps.
- No target code or target architecture was created.

## Explain

Why is tool access alone insufficient to define the analyst role? Why does the agent
load a skill for full discovery instead of repeating its procedure in the agent body?
Why must deterministic analysis remain subordinate to source and runtime evidence?

**Exit criterion:** Discovery is reviewable, or its blocking evidence is explicit.

Continue to [Lab 7](../07-handoffs-and-planning/README.md).