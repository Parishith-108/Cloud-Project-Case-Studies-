# Problem Statement

## Client environment

A global enterprise used Azure cloud extensively with applications deployed across Azure App Services, Azure Functions, Cosmos DB, and SQL Database. Authentication and authorization were managed through Azure Entra ID (formerly Azure AD), and encryption keys were stored in Azure Key Vault. However, secret and key management was fragmented: developers stored connection strings directly in configuration files, service principals had unlimited key rotation cycles, and there was no centralized vault for auditing or controlling access to sensitive material.

## Observed risks

- Application secrets and connection strings were scattered across multiple Azure App Settings, GitHub repositories (in secrets management files), and local developer machines.
- Azure Key Vault access policies were overly permissive; developers could read, create, and delete keys without approval workflows.
- No correlation between Azure Entra ID (identity provider) and the actual permissions granted in Key Vault; privilege creep was common.
- Service principal keys were rotated manually or on ad-hoc schedules, creating orphaned keys and compliance violations.
- CyberArk was deployed for on-premises secrets management but was not integrated with Azure; Azure secrets lived in a separate silo.
- When a developer left the organization, their service principal keys were not revoked immediately, exposing a window for unauthorized access.

## Critical incident

A disgruntled contractor with developer access used a 90-day-old service principal key (never rotated) to authenticate to an Azure SQL Database from outside the organization. The key was discovered in CyberArk's audit logs 3 days later when a security analyst reviewed access to a specific database. By then, the contractor had exfiltrated customer data from multiple tables. The incident revealed:

- Service principal keys were not being rotated on a predictable schedule.
- No automated key lifecycle management tied to employee identity.
- CyberArk and Azure had no shared audit trail; the contractor's access was not visible in real-time monitoring.
- Entra ID didn't enforce conditional access for service principal authentication from external networks.

## Business impact

If governance gaps persist, the organization risks:

- data exfiltration through stolen or orphaned service principal keys,
- compliance violations (SOC 2, ISO 27001) due to lack of centralized secret audit trails,
- inability to quickly revoke access for terminated employees or contractors,
- and regulatory fines if customer data is exposed due to inadequate key management.
