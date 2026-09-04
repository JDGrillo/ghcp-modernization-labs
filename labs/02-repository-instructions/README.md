# Lab 2: Repository instructions

**Modernization outcome:** Identify the policies that govern every lifecycle stage  
**Copilot primitive:** `.github/copilot-instructions.md`

## Learn

Repository instructions are always-on project policy. They answer **what must remain
true across the repository**, not how to perform one specialist workflow. Instructions
guide agent behavior; Lab 4 shows why a deterministic hook is still needed for a
high-value mutation boundary.

Open [`.github/copilot-instructions.md`](../../.github/copilot-instructions.md). Use
these policy groups to orient the demo:

| Policy group | Important repository requirements | Demo effect |
|---|---|---|
| Evidence | `legacy-source/` is immutable; facts, interpretations, assumptions, and gaps remain distinct | Copilot reads legacy artifacts without editing them or inventing missing evidence |
| Lifecycle | `modernization/<application-id>/lifecycle.json` and canonical indexes control stage and handoffs | Copilot checks lifecycle state before moving to planning or implementation |
| Architecture | An approved slice records one backend platform and its matching target root | Copilot does not mix Spring and .NET or generate code outside the selected target |
| Security and deployment | Azure uses reviewed Terraform, private connectivity, managed identity, and least privilege | Copilot does not substitute `azd`, public data access, or stored credentials |
| Approval and reporting | Agents cannot approve their own work; results must report actual pass, fail, skip, and blocked states | Copilot stops at ready for review and names missing gates rather than claiming completion |

## Exercise

1. Read the repository instructions using the five policy groups above. Locate the
   exact rule for each demo effect.
2. Re-run the bounded request from Lab 1. Correct the attribution column from Lab 1:
   distinguish constraints stated by the request from behavior required even if the
   prompt omitted it. Cite the exact repository-policy bullet for each latter claim.
3. Demonstrate lifecycle enforcement with this prompt:

   ```text
   Explain whether a React screen can be implemented directly from
   legacy-source/DEV1/SURVDEMO. Cite the repository policies and artifacts that must
   exist first. Do not create or edit files.
   ```

   The response should point to the lifecycle manifest, approved source-to-target
   mapping and plan, selected backend/target-root pair, tests and traceability, and
   required human approval. It should not start implementation.
4. Demonstrate deployment policy with this prompt:

   ```text
   From the repository instructions, summarize the required Azure deployment path
   and the controls that prohibit an azd-based or public-data-plane shortcut.
   ```

   The response should identify reviewed Terraform, the declared state profile,
   private data-plane connectivity, managed identities, policy and diagnostics, and
   approval bound to a saved-plan digest. Local state is limited to the disposable,
   single-user sandbox; shared or persistent environments require protected remote
   state and federated automation identity.

## Verify

Create a two-column note in chat:

| Always-on policy | Observable behavior |
|---|---|
| Legacy evidence is immutable | Copilot reads but does not edit source |
| Agents cannot approve their own work | Discovery stops at ready for review |
| Lifecycle artifacts control transitions | Copilot checks the manifest and canonical indexes before advancing |
| One backend and target root are selected | Copilot keeps generated code in the approved stack and location |
| Azure deployment uses reviewed Terraform | Copilot rejects `azd` and requires the prescribed deployment controls |

Confirm each row against the repository instructions and the two demo responses.
This table is the lab output; do not create a policy summary under `modernization/`.

## Explain

Why would putting the complete COBOL discovery procedure in repository instructions
waste context and blur responsibilities?

**Exit criterion:** You can distinguish durable policy from task procedure.

Continue to [Lab 3](../03-path-instructions/README.md).