---
applyTo: "target/react-spring-azure-sql/infrastructure/**,target/react-dotnet-azure-sql/infrastructure/**"
---

# Enterprise Azure infrastructure rules

- Use the `deploy-enterprise-azure-slice` skill and Terraform only. Never add or invoke `azd`.
- Pin Terraform and provider version constraints and commit the dependency lock file. Use reusable modules only where they express a real ownership or lifecycle boundary.
- Store shared-environment state in a separately bootstrapped, protected Azure Storage backend with versioning, soft delete, private access, locking, and workload identity federation. Never commit state, plan files, credentials, or generated secrets.
- Keep application ingress behind an approved HTTPS WAF edge. Disable public network access for application origins, Azure Container Registry, Key Vault, and Azure SQL.
- Make subnet delegation, private endpoints, private DNS zones and links, routes, network security controls, egress, and private operator/build-agent connectivity explicit.
- Use user-assigned managed identities for workloads, Microsoft Entra authentication for users and Azure SQL, federated workload identity for CI/CD, and least-privilege data-plane RBAC. Do not use SQL passwords, client secrets, access keys, or broad Owner assignments.
- Keep secrets in Key Vault and pass only secret references to workloads. Mark unavoidable Terraform outputs sensitive and do not expose protected values in logs or evidence.
- Enable diagnostic settings, distributed tracing, audit logs, actionable alerts, policy checks, security scanning, cost evidence, and retention appropriate to the environment.
- Protect stateful resources from accidental destruction and document tested backup, restore, migration, rollback, drift detection, ownership, and break-glass procedures.
- Run `terraform fmt -check`, `terraform validate`, tests, lint, security/policy checks, and plan review. Apply only an approved saved plan whose digest and environment match the lifecycle artifact; never use `terraform apply -auto-approve`.