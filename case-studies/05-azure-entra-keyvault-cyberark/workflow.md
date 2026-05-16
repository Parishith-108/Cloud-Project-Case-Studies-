# Implementation Workflow

This workflow describes the step-by-step process to integrate Azure Entra ID, Azure Key Vault, and CyberArk for unified secret management and automated key rotation.

## Phase 1: Audit and discovery (Week 1-2)

### Step 1.1: Inventory all secrets and service principals

- Export all service principals from Azure Entra ID using the Azure CLI or Portal:
  ```bash
  az ad sp list --query "[].{displayName:displayName, appId:appId, createdDateTime:createdDateTime}" -o json
  ```
- For each service principal, determine:
  - Which Azure resources it accesses (App Services, SQL Database, Key Vault, Cosmos DB, etc.).
  - The current authentication method (password, certificate, managed identity).
  - Last rotation date (if applicable).
  - Who created and owns it (business justification).
  - Risk tier (production-critical, development, test).

### Step 1.2: Catalog all secrets currently stored in Azure Key Vault

- Export Key Vault secrets:
  ```bash
  az keyvault secret list --vault-name "<vault-name>" --query "[].{name:name, updated:attributes.updated}" -o json
  ```
- For each secret, identify:
  - What it's used for (connection string, API key, certificate, etc.).
  - Which applications depend on it.
  - Rotation frequency (current vs. recommended).

### Step 1.3: Identify orphaned and over-privileged secrets

- Search GitHub and Azure DevOps repositories for hardcoded secrets (connection strings, keys, passwords).
- Review Azure Key Vault access policies to find overly permissive assignments (e.g., developers with full admin permissions).
- Flag service principals that have not been used in 90+ days.
- Create a risk assessment spreadsheet ranking secrets by sensitivity and compliance requirement.

## Phase 2: Azure Entra ID configuration (Week 2-3)

### Step 2.1: Enable Entra ID conditional access policies

- In the Azure Portal, navigate to Azure Entra ID > Security > Conditional Access.
- Create a policy targeting service principals:
  - **Condition**: Cloud apps = "Azure Key Vault" or "Azure Resource Manager"
  - **Condition**: Client type = "Service principals"
  - **Grant**: Require managed identity or certificate-based auth.
  - **Grant**: Require MFA or Entra ID verification for sensitive operations.

### Step 2.2: Enforce certificate-based service principal authentication

- For each service principal, create a certificate credential:
  ```bash
  az ad sp create-for-rbac --name "<app-name>" --cert --years 2
  ```
- Upload the certificate to Entra ID:
  ```bash
  az ad app credential reset --id "<app-id>" --cert "@cert.pem" --display-name "production-cert"
  ```
- Disable password/client secret credentials:
  ```bash
  az ad app credential delete --id "<app-id>" --key-id "<credential-id>"
  ```

### Step 2.3: Deploy managed identities for Azure resources

- For each Azure App Service or Azure Function, enable system-assigned managed identity:
  ```bash
  az appservice identity assign --resource-group "<rg>" --name "<app-name>" --identities "[system]"
  ```
- For stateless workloads, use user-assigned managed identities with role assignments scoped to specific Key Vault operations.

### Step 2.4: Set up Entra ID Privileged Identity Management (PIM) for CyberArk access

- Register CyberArk service principal in PIM as an eligible assignment:
  - Role: "Key Vault Administrator" (limited scope to CyberArk integration account).
  - Activation requires approval and MFA from a security team member.
  - Duration: 2 hours per session; audit log all activations.

## Phase 3: CyberArk configuration and integration (Week 3-4)

### Step 3.1: Set up CyberArk-Azure integration account

- Create a service principal in Entra ID for CyberArk's authentication:
  ```bash
  az ad sp create-for-rbac --name "CyberArk-Azure-Integration" --role "Key Vault Administrator"
  ```
- Store the service principal certificate in CyberArk's vault.
- In CyberArk's configuration, set the Entra ID authentication method to certificate-based.

### Step 3.2: Create CyberArk safe and platform for Azure secrets

- In CyberArk, create a new Safe: `Azure-App-Secrets`
- Define account platforms for:
  - Azure App Service connection strings
  - Azure SQL Database credentials
  - Azure Cosmos DB keys
  - Service principal client secrets/certificates
- Set retention policies: rotate every 30 days for service principals, every 60 days for database credentials.

### Step 3.3: Migrate existing secrets to CyberArk

- Use the CyberArk REST API to programmatically add secrets:
  ```bash
  curl -X POST "https://cyberark.company.com/PasswordVault/api/Accounts" \
    -H "Authorization: Bearer $TOKEN" \
    -d '{
      "safe": "Azure-App-Secrets",
      "platformID": "AzureSQL",
      "name": "sql-app-prod-connection",
      "password": "...",
      "username": "sqladmin@company.onmicrosoft.com",
      "address": "prodserver.database.windows.net"
    }'
  ```
- Verify each secret was successfully stored before removing it from Azure Key Vault.

### Step 3.4: Configure CyberArk rotation policies

- For each secret platform, define rotation frequency and rotation targets:
  - **Azure SQL Database credentials**: 60-day rotation via Azure SQL API.
  - **Service principal certificates**: 30-day rotation via Entra ID API.
  - **Cosmos DB keys**: 60-day rotation via Azure REST API.
- Test rotation in a dev environment first to ensure the rotation target is reachable and credentials are valid after rotation.

### Step 3.5: Configure CyberArk-to-Azure Key Vault sync

- In CyberArk, create a custom REST API call to sync rotated secrets to Azure Key Vault:
  ```json
  {
    "name": "Sync-Rotated-Secret-to-KeyVault",
    "trigger": "after-rotation",
    "azureKeyvaultVault": "company-kv-prod",
    "secretName": "{{ account.name }}",
    "secretValue": "{{ account.password }}"
  }
  ```
- This ensures Azure Key Vault is always in sync with CyberArk and applications retrieve the latest rotated secret.

## Phase 4: Azure Key Vault reconfiguration (Week 4-5)

### Step 4.1: Remove all shared access keys and static credentials

- Audit all applications currently using hardcoded connection strings from Key Vault:
  ```bash
  az keyvault secret list --vault-name "<vault-name>" --query "[?contains(name, 'connection')].name" -o json
  ```
- For each secret, update the application to retrieve it via:
  - Managed identity for Azure-native apps.
  - CyberArk API for hybrid/on-premises apps (with certificate-based CyberArk auth).

### Step 4.2: Update Key Vault access policies to use Entra ID only

- Remove all access policies that grant users direct permissions:
  ```bash
  az keyvault delete-policy --name "<vault-name>" --object-id "<user-object-id>"
  ```
- Add role assignments using Azure RBAC:
  ```bash
  az role assignment create --role "Key Vault Secrets Officer" \
    --assignee "<app-managed-identity-id>" \
    --scope "/subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.KeyVault/vaults/<vault-name>"
  ```

### Step 4.3: Enable key versioning and soft delete

- Enable soft delete and purge protection:
  ```bash
  az keyvault update --name "<vault-name>" --enable-soft-delete true --enable-purge-protection true
  ```
- Soft delete allows recovery of accidentally deleted secrets for 90 days.
- Purge protection prevents permanent deletion without a cooling-off period.

### Step 4.4: Enable diagnostic logging

- Configure Azure Key Vault to send all operations to Azure Monitor:
  ```bash
  az monitor diagnostic-settings create \
    --name "KeyVault-DiagLogs" \
    --resource "/subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.KeyVault/vaults/<vault-name>" \
    --logs "[{category:AuditEvent, enabled:true}]" \
    --workspace "/subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>"
  ```
- Send logs to CyberArk's SIEM integration or export to your log aggregation system.

## Phase 5: Application integration (Week 5-6)

### Step 5.1: Migrate Azure App Services to managed identity authentication

- Update App Service code to use managed identity:

  **C# example using DefaultAzureCredential:**
  ```csharp
  var credential = new DefaultAzureCredential();
  var client = new SecretClient(new Uri("https://<vault-name>.vault.azure.net/"), credential);
  KeyVaultSecret secret = await client.GetSecretAsync("<secret-name>");
  ```

  **Python example using azure-identity:**
  ```python
  from azure.identity import DefaultAzureCredential
  from azure.keyvault.secrets import SecretClient

  credential = DefaultAzureCredential()
  client = SecretClient(vault_url="https://<vault-name>.vault.azure.net", credential=credential)
  secret = client.get_secret("<secret-name>")
  ```

- Remove connection strings from app settings; Key Vault now provides them at runtime.

### Step 5.2: Migrate on-premises or hybrid workloads to CyberArk API

- For applications not running on Azure, configure them to fetch secrets from CyberArk:

  **Example Python script using CyberArk API:**
  ```python
  import requests

  cyberark_url = "https://cyberark.company.com"
  cert = ("<client-cert>.pem", "<client-key>.pem")

  # Authenticate to CyberArk
  auth_response = requests.post(f"{cyberark_url}/PasswordVault/api/auth/Certificates/Logon", cert=cert)
  token = auth_response.json()["CyberArkLogonResult"]

  # Retrieve secret
  headers = {"Authorization": f"Bearer {token}"}
  secret_response = requests.get(
      f"{cyberark_url}/PasswordVault/api/Accounts",
      headers=headers,
      params={"query": "name=sql-app-prod-connection"}
  )
  secret_id = secret_response.json()[0]["id"]

  # Get password
  password_response = requests.get(
      f"{cyberark_url}/PasswordVault/api/Accounts/{secret_id}/password",
      headers=headers
  )
  password = password_response.json()["Content"]
  ```

### Step 5.3: Test failover and secret rotation scenarios

- Manually trigger a CyberArk secret rotation and verify:
  - The new secret is synced to Key Vault within 5 minutes.
  - Applications retrieve the new secret on next access.
  - No application downtime or connection errors occur.
- Simulate a service principal key compromise:
  - Mark the old key as revoked in CyberArk.
  - Trigger an emergency rotation.
  - Verify all applications switch to the new key automatically.

## Phase 6: Monitoring, alerting, and lifecycle automation (Week 6-7)

### Step 6.1: Set up real-time alerting for unauthorized access

- Create Azure Monitor alerts:
  ```bash
  az monitor metrics alert create \
    --name "KeyVault-UnauthorizedAccess" \
    --resource-group "<rg>" \
    --scopes "/subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.KeyVault/vaults/<vault-name>" \
    --condition "total ServiceApiResult where ResultType == Unauthorized > 5 in 5m" \
    --description "Alert when Key Vault receives >5 unauthorized access attempts" \
    --action "<action-group-id>"
  ```

- In CyberArk, create custom alerts:
  - Alert if a secret is accessed more than 10 times in 1 hour.
  - Alert if a secret is accessed from an IP outside the corporate network.
  - Alert if rotation fails 3 consecutive times (indicates stale password or API issue).

### Step 6.2: Automate employee offboarding

- Create an Azure Logic App or Function that triggers when an employee is terminated in Entra ID:
  - Remove the employee's service principal from Entra ID and Key Vault.
  - Delete all associated service principal keys from CyberArk.
  - Rotate any database/app passwords the employee had access to.
  - Log all actions to the audit trail.

  **Example Logic App flow:**
  ```
  Trigger: When an employee is removed from Entra ID
  -> Query CyberArk for all secrets owned by that employee
  -> For each secret:
    -> Rotate the secret
    -> Revoke Entra ID role assignments
    -> Log to SIEM
  -> Send email confirmation to security team
  ```

### Step 6.3: Quarterly secret and key reviews

- Generate a report of all active service principals and their last rotation date:
  ```bash
  az ad sp list --query "[].{displayName:displayName, createdDateTime:createdDateTime}" -o json > sp-inventory.json
  ```
- Compare against the CyberArk rotation log to identify any secrets over the rotation threshold.
- Schedule reviews with each application owner to confirm access is still needed.

## Phase 7: Validation and cutover (Week 7-8)

### Step 7.1: Run parallel testing in production

- For 2 weeks, run both the old secret retrieval method (direct Key Vault) and the new method (CyberArk-synced Key Vault) in parallel.
- Monitor application logs for any differences in secret values or access patterns.
- If discrepancies are found, delay cutover and investigate.

### Step 7.2: Communicate change to application teams

- Provide runbooks for each team:
  - How to retrieve secrets from Key Vault using managed identity.
  - How to report access issues or rotation failures.
  - How to request emergency key rotation.
  - Escalation contacts (on-call security engineer).

### Step 7.3: Decommission old secret storage

- Once all applications have transitioned:
  - Remove any hardcoded secrets from GitHub, Azure DevOps, and config files.
  - Delete orphaned secrets from Key Vault.
  - Archive old Key Vault access logs for compliance.
  - Document the transition in the security wiki.

## Timeline summary

- **Weeks 1-2**: Audit and discovery
- **Weeks 2-3**: Azure Entra ID configuration
- **Weeks 3-4**: CyberArk configuration and integration
- **Weeks 4-5**: Azure Key Vault reconfiguration
- **Weeks 5-6**: Application integration
- **Weeks 6-7**: Monitoring and automation
- **Weeks 7-8**: Validation and cutover

**Total: 8 weeks from start to full production deployment.**
