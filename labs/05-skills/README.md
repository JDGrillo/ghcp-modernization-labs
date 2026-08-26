# Lab 5: Skills and bundled specialist resources

**Modernization outcome:** Understand the reusable discovery procedure before running it  
**Copilot primitive:** `.github/skills/<skill-name>/SKILL.md`

## Learn

A skill packages a repeatable multi-step method with scripts, references, templates,
and stopping conditions. Its description determines when it is discovered. Skills
describe **how specialist work is performed**; agents determine who owns the work and
which tools and boundaries apply.

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

   Confirm it analyzes all three sample applications twice and compares deterministic
   output without writing to `legacy-source/`.
6. Inspect the analyzer contract. Identify stable source coordinates and IDs, coverage,
   limitations, diagnostics, and the `candidate-evidence-only` capability. Explain why
   unresolved dynamic calls and missing copybooks become warnings rather than guesses.
7. Distinguish the complete discovery procedure from a narrowly scoped request to trace
   one entry point. The former needs the skill; the latter can be handled by the owning
   agent without creating the full evidence package.
8. Inspect the planning, implementation, validation, and enterprise Azure deployment
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

Produce this comparison in chat:

| Concern | Scoped agent request | Discovery skill |
|---|---|---|
| Scope | One named entry point | Whole application discovery |
| Output | Preliminary chat-only evidence map | Durable evidence package |
| Assets | Agent role and read/search tools | References, deterministic scripts, reconciliation, and templates |
| Lifecycle effect | None | Creates discovery artifacts and status |

Also report the analyzer test result and classify each extracted structure as
`analyzer-observed`, `heuristic`, `analyst-confirmed`, or `unresolved`.

## Explain

Why should detailed COBOL analysis guidance live in a skill reference rather than the
Legacy Analyst agent body? Why should a narrow reconnaissance request not automatically
create lifecycle artifacts? Why is deterministic candidate evidence useful but
insufficient for approval or parity?

**Exit criterion:** You can explain skill discovery, progressive resource loading, and
the skill-versus-agent boundary.

Continue to [Lab 6](../06-custom-agent-discovery/README.md).