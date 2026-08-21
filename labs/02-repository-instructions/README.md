# Lab 2: Repository instructions

**Modernization outcome:** Identify the policies that govern every lifecycle stage  
**Copilot primitive:** `.github/copilot-instructions.md`

## Learn

Repository instructions are always-on project policy. They answer **what must remain
true across the repository**, not how to perform one specialist workflow.

## Exercise

1. Before opening `.github/copilot-instructions.md`, predict five policies that must
   apply to discovery, planning, implementation, validation, and deployment.
2. Inspect the file and classify each rule as evidence, lifecycle, architecture,
   security, or reporting policy.
3. Re-run the bounded request from Lab 1 and identify visible effects of the policy.
4. Ask Copilot to implement a React screen directly from `SURVDEMO` without discovery
   or a plan. Observe which repository policies prevent that transition.
5. Find the rules covering human approval, the canonical lifecycle manifest, the
   selected backend/target-root pair, and Terraform-only Azure deployment.

## Verify

Create a two-column note in chat:

| Always-on policy | Observable behavior |
|---|---|
| Legacy evidence is immutable | Copilot reads but does not edit source |
| Agents cannot approve their own work | Discovery stops at ready for review |

Add at least three more rows from your observations.

## Explain

Why would putting the complete COBOL discovery procedure in repository instructions
waste context and blur responsibilities?

**Exit criterion:** You can distinguish durable policy from task procedure.

Continue to [Lab 3](../03-path-instructions/README.md).