---
name: deploy-enterprise-azure-slice
description: "Plan and deploy an enterprise React, selected Java or .NET backend, and Azure SQL slice with Terraform, private networking, Entra identity, policy, diagnostics, approval, drift, and rollback. Never use azd."
user-invocable: false
---

# Deploy Enterprise Azure Slice

Keep infrastructure planning, authorization, deployment, and independent validation as separate evidence gates.

## Entry identities

Require `modernization/<application-id>/lifecycle.json`. Bind every artifact and command to its application ID, source revision, active slice revisions, backend platform, target root, target revision, Terraform revision, environment ID, Azure tenant/subscription, and deployment run ID. Never record credentials or access tokens.

## Procedure

1. Retrieve current Azure general deployment guidance and Azure Terraform best practices. Verify Terraform is installed and record its version; never invoke `azd`.
2. Run the lifecycle validator with `--transition to-deployment-plan`. Stop unless independent validation passed for the exact target revision.
3. Record or verify an approved architecture decision covering region, environment classification, subscriptions, resource groups, naming, tags, availability, recovery objectives, data residency, DNS ownership, IP ranges, ingress/egress, build-agent connectivity, identity owners, policy assignments, logging, retention, budgets, and rollback.
4. Bootstrap remote Terraform state separately with versioning, soft delete, encryption, private access, locking, and narrowly scoped workload identity federation. Never put backend credentials in source or a plan artifact.
5. Implement reviewed Terraform with pinned Terraform/provider constraints, environment-specific variables, deterministic naming, lifecycle protections for stateful resources, and no secrets in variables or outputs.
6. Require a WAF-controlled HTTPS edge. Disable public network access on application origins, Azure Container Registry, Key Vault, and Azure SQL. Configure delegated subnets or private endpoints, private DNS zones and links, network security controls, explicit egress, and an approved private deployment-agent path.
7. Configure user-assigned managed identities and least-privilege RBAC for image pull, Key Vault secret retrieval, monitoring, and other data-plane access. Configure Microsoft Entra user authentication and backend authorization. Use Entra token authentication to Azure SQL and provision contained database roles through an approved, audited bootstrap process.
8. Enable diagnostic settings, Application Insights or approved OpenTelemetry export, Log Analytics, actionable alerts, audit retention, Defender and policy controls required by the environment, resource locks where appropriate, and budgets. Redact protected data.
9. Run formatting, `terraform validate`, lint, security/policy checks, tests, and a speculative plan. Generate a saved plan only in protected CI or a secured private operator environment. Review replacements, deletes, role grants, network exposure, policy exceptions, costs, sensitive outputs, Azure SQL retention, and protections against accidental database destruction.
10. Write the canonical deployment-plan artifact with exact commands, tool versions, results, Terraform revision, saved-plan SHA-256 digest, expiry, controls, exceptions, cost evidence, rollback, and approver roles. Update lifecycle to deployment/`planned`, set approval to pending, and stop.
11. After an accountable human or external process records approval for that exact digest and environment, run `--transition to-deployment-apply`. Recreate the plan if code, variables, providers, state, target revision, environment, or approval scope changed.
12. Apply the exact reviewed saved plan without `-auto-approve`. Do not apply an unreviewed speculative plan. Capture exit status and state serial without storing sensitive plan or state content in evidence.
13. Before migration, verify the exact source snapshot, target schema version, protected backup/PITR point, restore rehearsal, capacity, and reconciliation/recovery plans. Run the approved migration with a separate short-lived least-privilege Entra migration identity. Stop on checksum/snapshot drift, unmapped or lossy transformation, unowned rejects, or tolerance breach. Verify reconciliation before releasing any source freeze, then verify DNS, denied public access, TLS, application flow, authorization, audit, diagnostics, alerts, scale, and recovery probes.
14. Write the canonical deployment report with the durable approval reference, update lifecycle to deployment/`deployed`, reset the lifecycle approval object to pending so it cannot authorize another apply, and run `--transition to-azure-validation` before handing off to the Validation Critic.

## Stop conditions

Stop on a changed plan digest, missing approval, public data-plane exposure, credential-based automation, excessive RBAC, unresolved policy denial, absent private DNS/connectivity, destructive change without approved recovery, failed migration or reconciliation, source-snapshot drift, unowned rejects, failed security check, or incomplete audit evidence. A successful apply proves resource convergence only; it does not prove schema correctness, data parity, or production readiness.

Use [the enterprise topology reference](./references/enterprise-topology.md) as the lab
default and review checklist. Replace it only through an approved architecture decision
that preserves equivalent trust boundaries and controls.