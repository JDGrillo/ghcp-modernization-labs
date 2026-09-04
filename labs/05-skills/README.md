# Lab 5: Skills and bundled specialist resources

**Modernization outcome:** Understand the reusable discovery procedure before running it  
**Copilot primitive:** `.github/skills/<skill-name>/SKILL.md`

## Learn

A skill packages a repeatable multi-step method with scripts, references, templates,
and stopping conditions. Its description determines when it is discovered. Skills
describe **how specialist work is performed**; agents determine who owns the work and
which tools and boundaries apply. Lab 6 demonstrates that ownership and invocation
decision; this lab inspects the skill itself without creating discovery artifacts.

Use [the discovery skill](../../.github/skills/discover-mainframe-application/SKILL.md)
as the primary artifact. Its `references/` files provide specialist guidance, its
`scripts/` files provide deterministic candidate analysis, and its procedure and stop
conditions govern the durable discovery package.

## Exercise

1. Inspect the discovery skill.
2. Identify its entry conditions, ordered procedure, minimum outputs, and prohibited
   outcomes.
3. Inspect the bundled resources:
   - `references/legacy-analysis.md`;
   - `references/automated-cobol-analysis.md`;
   - `references/zowe-extraction.md`;
   - `scripts/inventory_sources.py`;
   - `scripts/analyze_cobol.py` and `scripts/test_analyze_cobol.py`.
4. Use the skill's ordered procedure to record where each resource is loaded and the
   task it supports. Resources not named by the active step remain unloaded.
5. Run the analyzer regression suite:

   ```powershell
   python -B .github/skills/discover-mainframe-application/scripts/test_analyze_cobol.py
   ```

   The expected result is 4 passing tests and exit code 0. One test analyzes each of
   the three sample applications twice and compares deterministic output without
   writing to `legacy-source/`. Stop on a failure; Lab 6 must not rely on a failing
   analyzer.
6. Inspect the analyzer contract. Identify stable source coordinates and IDs, coverage,
   limitations, diagnostics, and the `candidate-evidence-only` capability. Explain why
   unresolved dynamic calls and missing copybooks become warnings rather than guesses.
7. Inspect the planning, implementation, validation, and enterprise Azure deployment
   skill descriptions without running them. Use this ownership map in the demo:

   | Skill | Owning agent | Lifecycle responsibility |
   |---|---|---|
   | `plan-mainframe-modernization` | Modernization Planner | Produce an approved, bounded slice plan |
   | `implement-mainframe-slice` | Java or .NET Implementation Agent | Implement only the approved target slice |
   | `validate-mainframe-modernization` | Validation Critic | Independently evaluate parity and readiness evidence |
   | `deploy-enterprise-azure-slice` | Azure Deployment Agent | Plan and execute approval-controlled Terraform deployment |

   Deployment remains separate because infrastructure authority, saved-plan approval,
   apply, drift, and rollback are not implementation responsibilities.

## Verify

Produce this resource map in chat:

| Skill element | Purpose | Loaded or run at which discovery step? | Evidence limit |
|---|---|---|---|
| `SKILL.md` procedure | | | |
| `legacy-analysis.md` | | | |
| `automated-cobol-analysis.md` | | | |
| `zowe-extraction.md` | | | |
| `inventory_sources.py` | | | |
| `analyze_cobol.py` | | | |

Also report the analyzer test result and classify each extracted structure as
`analyzer-observed`, `heuristic`, `analyst-confirmed`, or `unresolved`.

## Explain

Why should detailed COBOL analysis guidance live in a skill reference rather than the
Legacy Analyst agent body? Why are optional references loaded only for the discovery
step that needs them? Why is deterministic candidate evidence useful but insufficient
for approval or parity?

**Exit criterion:** You can explain skill discovery, progressive resource loading, and
the skill-versus-agent boundary.

Continue to [Lab 6](../06-custom-agent-discovery/README.md).