# Architecture Decision

## Decision summary

Integrate Azure Entra ID, Azure Key Vault, and CyberArk into a unified secret and key management architecture where all service principal keys and application secrets are centrally stored in CyberArk, rotated on strict schedules, and synchronized with Azure Key Vault. Azure Entra ID will enforce identity-based access controls and conditional access policies to prevent unauthorized service principal usage.

## Decision details

### Identity and access layer (Azure Entra ID)

- Define application and service principal identities in Entra ID with strict naming conventions.
- Enforce Entra ID conditional access policies requiring:
  - Managed identity or certificate-based authentication (not password or key-based).
  - Sign-in restrictions: apps must authenticate from Azure-managed networks only.
  - Time-based step-up authentication for sensitive keys (CyberArk vault access requires MFA).
- Implement Entra ID Privileged Identity Management (PIM) for temporary, just-in-time access to sensitive key operations.
- Disable password-based authentication for service principals; enforce certificate-based or managed identity workflows.

### Secret and key management layer (CyberArk + Azure Key Vault)

- Deploy CyberArk as the system of record for all secrets, passwords, and keys.
- Store service principal certificates and client secrets in CyberArk with metadata linking to Entra ID application IDs.
- Configure CyberArk rotation policies for each service principal:
  - Azure service principals: rotate every 30 days.
  - Database connection strings: rotate every 60 days.
  - API keys: rotate every 90 days.
- Use CyberArk's REST API to automatically update Azure Key Vault with rotated secrets on each rotation cycle.
- Implement CyberArk's Azure integration plugin to authenticate as a managed identity to Azure, eliminating static credentials.

### Application layer (Azure Key Vault access)

- Configure Azure Key Vault to use Entra ID for all access control (not shared access keys).
- Grant applications access to Key Vault only via managed identities; never use connection strings hardcoded in app settings.
- Implement time-bound access: Azure Functions and App Services authenticate using managed identities with role assignments scoped to specific Key Vault operations.
- Enable Azure Key Vault diagnostic logging to send all get, set, and delete operations to Azure Monitor and CyberArk.

### Rotation and lifecycle automation

- CyberArk rotates service principal keys on schedule (every 30 days).
- A CyberArk REST API call synchronizes the rotated key to Azure Key Vault.
- Azure Key Vault versioning preserves old versions for 30 days to allow rollback if rotation fails.
- When an employee or contractor is terminated in Entra ID, a workflow removes their associated service principal from CyberArk and revokes Key Vault access within 1 hour.

### Monitoring and incident response

- CyberArk sends all key/secret access events to Azure Monitor and a Security Information and Event Management (SIEM) system.
- Real-time alerts trigger if:
  - A service principal authenticates from an unexpected IP or location.
  - A key is accessed more than 5 times in 1 minute (brute force pattern).
  - An access attempt fails 3 times consecutively (compromised key indicator).
- Automated response: immediately rotate the suspected key and alert the security team.

## Why this approach

- Centralized vault (CyberArk) eliminates silos between on-premises and cloud secrets.
- Entra ID conditional access prevents unauthorized service principal usage even if a key is stolen.
- Automated rotation ensures keys are never stale or inherited by future users.
- Managed identities eliminate the need for static credentials in application code.
- Real-time monitoring and alerting catch compromised keys within minutes instead of days.
- Termination workflows ensure no orphaned access for departed employees.
