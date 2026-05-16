# Tradeoffs

## Considered options

### Option 1: Centralized CyberArk + Azure Entra ID + Key Vault integration (chosen)

**Pros:**
- Single system of record (CyberArk) eliminates secret silos between on-premises and cloud.
- Automated rotation with CyberArk-to-Key-Vault sync keeps applications secure.
- Entra ID conditional access prevents unauthorized service principal usage even if keys are stolen.
- Real-time monitoring catches compromises within minutes.
- Managed identities eliminate static credentials from application code.

**Cons:**
- Requires 8 weeks of implementation effort and significant infrastructure changes.
- Adds operational complexity: teams must manage CyberArk, Key Vault, and Entra ID together.
- Rotation failures in CyberArk can cascade to Key Vault and disrupt applications if not handled gracefully.
- CyberArk licensing cost increases with additional Azure integrations and API usage.

**Cost estimate:** $150K (setup) + $50K/year (CyberArk licensing and Azure infrastructure).

---

### Option 2: Key Vault only with manual rotation and access policies

**Pros:**
- Simpler to implement; uses only native Azure services.
- Lower licensing cost (only Key Vault storage).
- Shorter time to production (4-6 weeks).

**Cons:**
- No correlation between Entra ID identities and Key Vault permissions; privilege creep continues.
- No automated rotation; manual processes are error-prone and slow.
- On-premises applications cannot use Key Vault; forced to maintain separate secrets silos.
- No advanced monitoring or anomaly detection (CyberArk provides).
- Contractor/employee offboarding remains a manual, high-risk process.
- Rejected because it does not address the core incident: unauthorized service principal key usage.

**Cost estimate:** $20K (setup) + $10K/year (Key Vault storage).

---

### Option 3: Managed identities only (no service principals)

**Pros:**
- Eliminates service principal key management entirely; no rotation needed.
- Lowest operational overhead and highest security.
- Works seamlessly for all Azure-native workloads.

**Cons:**
- Not applicable for on-premises, hybrid, or third-party cloud applications.
- Requires significant application refactoring to support managed identities.
- Some legacy systems cannot be updated to use managed identities.
- Rejected as the sole solution because the enterprise has hybrid and multi-cloud workloads.

**Adopted as a complementary approach:** Use managed identities for all Azure-native apps; combine with CyberArk for on-premises and hybrid workloads.

**Cost estimate:** $30K (refactoring).

---

### Option 4: Azure AD B2C + shared access keys for applications

**Pros:**
- Avoids service principal complexity; uses user-based access.
- Reduced overhead compared to service principal management.

**Cons:**
- Still requires rotating shared access keys; no automation.
- Azure AD B2C is designed for customer identity, not application-to-resource authentication.
- Cannot enforce fine-grained access controls (e.g., read-only vs. admin).
- Rejected because it conflates user identity with application identity management.

---

## Tradeoff analysis

| Dimension | Option 1 (Chosen) | Option 2 | Option 3 | Option 4 |
|-----------|---|---|---|---|
| **Security** | Highest; prevents unauthorized access via conditional access + rotation | Medium; relies on manual processes | Highest for Azure-native apps; incomplete for hybrid | Low; inadequate controls |
| **Automation** | Full; rotation, monitoring, offboarding all automated | Manual; error-prone | Full for managed identities only | Partial; still manual rotation |
| **Compliance** | Excellent; centralized audit trail and drift detection | Good; Key Vault logging available | Excellent for audit trail; limited scope | Fair; incomplete visibility |
| **Implementation time** | 8 weeks | 4-6 weeks | 6-8 weeks (app refactoring) | 3-4 weeks |
| **Operational complexity** | High (3 systems: CyberArk, Entra ID, Key Vault) | Low (1 system: Key Vault) | Medium (2 systems: Entra ID, managed identities) | Low (1-2 systems) |
| **Cost** | $150K + $50K/year | $20K + $10K/year | $30K refactoring + $5K/year | $15K + $8K/year |
| **Hybrid/on-premises support** | Excellent (CyberArk handles both) | Poor (Key Vault is Azure-only) | Poor (managed identities are Azure-only) | Poor |
| **Disaster recovery** | Excellent (CyberArk + Key Vault backup) | Medium (Key Vault geo-redundancy) | Medium (geo-redundancy) | Medium |

---

## Key decision drivers

1. **Incident prevention**: The contractor data exfiltration incident proved that manual key rotation and access controls are insufficient. Option 1 is the only solution that would have prevented this incident.

2. **Hybrid workload support**: The enterprise has on-premises applications that cannot use managed identities or Key Vault. CyberArk is the only solution that bridges this gap.

3. **Compliance requirements**: Auditors require a centralized, auditable secret management system. Option 1 (CyberArk) satisfies this; Option 2 does not.

4. **Long-term ROI**: Although Option 1 has a high upfront cost, the automated rotation and monitoring eliminate costly manual processes and incident response over time. Within 2 years, the cost of Option 1 is lower than the cost of managing Option 2 with additional tooling and incident remediation.

5. **Employee lifecycle**: Option 1's automated offboarding prevents orphaned access for departed contractors, which was the root cause of the original incident.

---

## Risk mitigation for chosen option

**Risk: Rotation failures disrupt applications**
- Mitigation: Implement health checks in applications; if Key Vault returns stale secrets, applications fall back to cached values or return a service degradation error instead of crashing.

**Risk: CyberArk becomes a single point of failure**
- Mitigation: Deploy CyberArk in a high-availability configuration with automatic failover. Maintain a backup CyberArk instance in a geographically separate data center.

**Risk: Entra ID conditional access policies are misconfigured**
- Mitigation: Implement policies in report-only mode first; validate that no legitimate applications are blocked before enforcing the policies.

**Risk: Migration to CyberArk API breaks legacy applications**
- Mitigation: Run both secret sources (CyberArk and Key Vault) in parallel for 2 weeks before cutover; monitor for any access anomalies.
