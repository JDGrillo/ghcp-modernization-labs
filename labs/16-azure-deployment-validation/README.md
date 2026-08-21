# Lab 16: Approved deployment and Azure validation

**Modernization outcome:** An applied Terraform plan plus independent, claim-limited
Azure evidence  
**Copilot primitive:** Human-gated agent execution and independent critic handoff

## Prerequisites

- Lab 15 left lifecycle at deployment/`planned` with a protected saved-plan digest.
- The plan remains current and an accountable approver can authorize that exact digest
   and environment. If either condition is false, return to Lab 15 and replan.

## Learn

Plan, apply, and validation are separate trust boundaries. Human approval names the
environment and saved-plan digest. The deployment agent may converge that exact plan;
the critic, in a fresh context, decides what the resulting Azure evidence supports.

## Exercise

1. Have an accountable human or external approval process review the plan and set the
   lifecycle approval fields. The deployment agent must not write the approval.
2. Run the lifecycle validator with `--transition to-deployment-apply`. Replan and
   repeat approval if code, inputs, providers, state, target, environment, or digest
   changed.
3. Apply the exact saved plan without `-auto-approve`. Record the state serial, resource
   IDs, command result, and approval reference without exposing state or secrets.
4. Verify the exact source snapshot, schema checksum, protected backup/PITR reference,
   restore rehearsal, capacity, migration lock, and target preconditions. Run migrations
   with a separate short-lived least-privilege Entra migration identity. Do not use a
   SQL password or the application identity when a distinct migration identity is
   required by the approved plan.
5. Verify private DNS, denied public access, TLS/WAF ingress, frontend-to-backend and
   backend-to-SQL flow, user authorization, least-privilege identity access, audit,
   diagnostics, alerts, scale, schema metadata, row counts, exact control totals,
   canonical hashes, rejected rows, backup/restore evidence, and recovery probes. Do
   not release a source freeze while reconciliation is failed or blocked.
6. Write `deployment-report.json`, set lifecycle to deployment/`deployed`, reset any
   consumed approval according to the lab process, and run the lifecycle validator
   with `--transition to-azure-validation`.
7. Use **Validate the Azure deployment**. The Validation Critic reruns applicable
   checks and writes a new Azure validation run; it does not repair findings.
8. Keep verdicts narrow: Terraform convergence, private connectivity, Azure SQL
   compatibility, application behavior, resilience, production readiness, and cutover
   authority are distinct claims.

## Gate

Failed identity, network, policy, migration, security, observability, recovery, or
application checks block readiness. Snapshot drift, silent coercion, an unmapped field,
unowned reject, or tolerance breach also blocks readiness. A rollback must return to a
known target and reconciled data state; `terraform destroy` is not a sufficient
production rollback strategy.

**Exit criterion:** The exact deployment has an independent Azure validation report
and lifecycle verdict, unresolved risks and exceptions have owners, and no agent has
self-approved readiness or cutover.

Continue to [Lab 17](../17-orchestrator-capstone/README.md).