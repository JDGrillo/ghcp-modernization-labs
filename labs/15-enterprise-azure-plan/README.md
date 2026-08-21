# Lab 15: Enterprise Azure architecture and plan

**Modernization outcome:** A reviewable, revision-bound Terraform plan for a private
Azure environment  
**Copilot primitive:** Dedicated deployment agent, deployment skill, and infrastructure
path instructions

## Prerequisites

- Lab 14 produced a passed validation report for the exact target revision.
- `validate_lifecycle.py --transition to-deployment-plan` passes.
- The Azure, Terraform, remote-state, private-network, DNS, identity, and approval
   prerequisites from Lab 0 are available; otherwise record the lab blocked.

## Learn

Deployment is its own lifecycle stage. The Azure Deployment Agent combines a scoped
role with a reusable procedure; path instructions constrain every generated Terraform
file. Deterministic lifecycle validation prevents an agent from deploying an
unvalidated target or approving its own plan.

The lab default is an HTTPS WAF edge with private application origins and private
connectivity to Azure Container Registry, Key Vault, and Azure SQL. Runtime access uses
managed identities and Microsoft Entra tokens. CI/CD uses workload identity federation,
not stored credentials. An approved ADR may substitute equivalent controls.

## Exercise

1. Inspect the Azure Deployment Agent, `deploy-enterprise-azure-slice` skill, Azure
   infrastructure instructions, and deployment artifact templates.
2. Confirm independent validation passed for the exact target revision and run the
   lifecycle validator with `--transition to-deployment-plan`.
3. Record the environment, subscription, region, data classification, network CIDRs,
   DNS owners, ingress/egress, recovery objectives, identity owners, policies, logging,
   retention, budget, and private build-agent path in an ADR. Do not invent them.
4. Invoke **Prepare an Azure deployment plan**. Confirm it retrieves current Azure and
   Terraform guidance and does not invoke `azd`.
5. Review generated Terraform under
   `<activeSlice.targetRoot>/infrastructure/`. Require remote state, pinned
   constraints, WAF ingress, denied public origins, private endpoints and DNS, managed
   identities, Entra authentication, least-privilege RBAC, diagnostics, policy checks,
   backup, and rollback.
6. Run format, validate, lint, tests, security/policy scans, cost estimation, and a
   speculative plan. A secured CI runner or private operator path is required for a
   saved plan that reaches private control or data planes.
7. Inspect replacements, deletes, grants, exposure, exceptions, cost, and sensitive
   outputs. Store the saved plan only as a protected short-lived artifact and record
   its SHA-256 digest in `deployment-plan.json`.
8. Bind the exact migration revision, protected source snapshot and pre-migration
   backup references, successful restore rehearsal, reconciliation plan, recovery
   runbook, retention, and database lifecycle protections into the deployment plan.
9. Confirm the agent updated lifecycle to deployment/`planned`, referenced the canonical
   deployment plan, reset approval to pending, and stopped. The validator checks state;
   it does not perform this mutation.

## Gate

The plan must bind application, source, slice, target, Terraform, environment, and
saved-plan identities. Any public data-plane access, stored credential, broad role,
unowned DNS/federation, failed scan, destructive unprotected change, or missing private
runner path blocks approval. So does a missing restore rehearsal, mutable source
snapshot, unresolved mapping, unowned reject, or unapproved reconciliation tolerance.

**Exit criterion:** An accountable reviewer can approve or reject one immutable plan
without reading conversational history, and no Azure resources have been changed.

Continue to [Lab 16](../16-azure-deployment-validation/README.md).