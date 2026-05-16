# Azure Entra ID + Key Vault + CyberArk Architecture Diagrams

This folder contains detailed diagrams illustrating the unified secret management architecture.

## Diagram 1: Incident Timeline (Before vs. After)

```mermaid
timeline
    title Contractor Key Exfiltration Incident: Before vs. After Implementation
    
    section BEFORE (Manual Key Management)
        Day 0 (T+0 hours)
            : Contractor leaves company
            : Service principal key never rotated
            : Key remains valid and stored in multiple locations
        
        Day 1 (T+24 hours)
            : Contractor uses 90-day-old key from external IP
            : API calls successful
            : SQL data exfiltration begins
        
        Day 3 (T+72 hours)
            : Security analyst manually reviews CyberArk logs
            : Unauthorized access detected
            : Key finally revoked and rotated
            : Data already exfiltrated
    
    section AFTER (Automated with CyberArk + Entra ID)
        Day 0 (T+0 minutes)
            : Employee terminated in Entra ID
            : Automated workflow removes service principal
            : CyberArk rotates key immediately
        
        Day 0 (T+5 minutes)
            : Key Vault updated with new rotated key
            : Old key marked as invalid
            : Access completely revoked
        
        Day 0 (T+10 minutes)
            : Contractor attempts login with old key
            : Entra ID conditional access rejects (invalid cert)
            : CloudWatch alert triggered
            : Security team notified in real-time
```

---

## Diagram 2: Architecture Overview - Azure Entra ID + CyberArk + Key Vault

```mermaid
graph TB
    subgraph EntraID["Azure Entra ID (Identity & Access)"]
        direction TB
        SP1["Service Principals"]
        SP2["User Identities"]
        CA["Conditional Access Policies"]
        PIM["Privileged Identity Management"]
        CA -->|Enforces| SP1
        PIM -->|Manages| SP1
    end
    
    subgraph CyberArk["CyberArk Vault (System of Record)"]
        direction TB
        SAFE1["Safe: Azure-App-Secrets"]
        SAFE2["Safe: Database-Credentials"]
        SAFE3["Safe: API-Keys"]
        ROT["Rotation Engine"]
        SAFE1 --> ROT
        SAFE2 --> ROT
        SAFE3 --> ROT
    end
    
    subgraph KeyVault["Azure Key Vault"]
        direction TB
        KV1["Synced Secrets"]
        KV2["Synced DB Passwords"]
        RBAC["RBAC Access Control"]
        RBAC --> KV1
        RBAC --> KV2
    end
    
    subgraph Applications["Applications & Workloads"]
        direction TB
        APP1["Azure App Service"]
        APP2["Azure Functions"]
        APP3["On-Premises App"]
        APPDB["SQL Database"]
        APPCOS["Cosmos DB"]
    end
    
    subgraph Monitoring["Monitoring & Alerting"]
        direction TB
        MONITOR["Azure Monitor + Alerts"]
        SIEM["SIEM Integration"]
        LOGS["Audit Logs"]
    end
    
    EntraID -->|Authenticates| CyberArk
    EntraID -->|Controls Access| KeyVault
    
    CyberArk -->|Rotates & Syncs| KeyVault
    CyberArk -->|Provides Secrets| APP3
    
    KeyVault -->|Managed Identity| APP1
    KeyVault -->|Managed Identity| APP2
    
    APP1 --> APPDB
    APP1 --> APPCOS
    
    CyberArk --> MONITOR
    KeyVault --> MONITOR
    Applications --> MONITOR
    
    MONITOR --> SIEM
    MONITOR --> LOGS
```

---

## Diagram 3: Secret Lifecycle Workflow (30-Day Rotation Cycle)

```mermaid
graph LR
    subgraph Day["Day 0-29: Secret Valid"]
        A["Secret stored in CyberArk"]
        B["Synced to Key Vault"]
        C["Applications use secret"]
        A --> B
        B --> C
    end
    
    subgraph Rotation["Day 30: Automated Rotation"]
        D["CyberArk rotation engine triggers"]
        E["New secret generated"]
        F["Old secret backed up"]
        G["New secret stored in CyberArk"]
        D --> E
        E --> F
        F --> G
    end
    
    subgraph Sync["Day 30: Sync to Key Vault"]
        H["REST API call to Key Vault"]
        I["New secret uploaded"]
        J["Old version preserved"]
        H --> I
        I --> J
    end
    
    subgraph AppUpdate["Day 30-31: Application Update"]
        K["App checks Key Vault on next request"]
        L["New secret retrieved"]
        M["Old secret no longer valid"]
        K --> L
        L --> M
    end
    
    subgraph Audit["Day 30+: Audit Trail"]
        N["Rotation logged in CyberArk"]
        O["Key Vault versioning recorded"]
        P["CloudTrail captures all changes"]
        N --> O
        O --> P
    end
    
    C --> D
    G --> H
    J --> K
    M --> N
```

---

## Diagram 4: Entra ID Conditional Access Flow

```mermaid
flowchart TD
    A["Service Principal attempts<br/>to access Key Vault"]
    
    B{"Is the identity<br/>in Entra ID?"}
    C["DENY: Identity not found"]
    
    D{"Is it using<br/>certificate-based auth?"}
    E["DENY: Only password/key auth used"]
    
    F{"Is MFA enabled<br/>for this principal?"}
    G["CHALLENGE: Require MFA"]
    
    H{"Is the login from<br/>a trusted network?"}
    I["CHALLENGE: Step-up authentication"]
    
    J["ALLOW: Access granted<br/>with audit logging"]
    
    A --> B
    B -->|No| C
    B -->|Yes| D
    D -->|No| E
    D -->|Yes| F
    F -->|No| G
    F -->|Yes| H
    H -->|No| I
    H -->|Yes| J
    
    style A fill:#e1f5ff
    style J fill:#c8e6c9
    style C fill:#ffcdd2
    style E fill:#ffcdd2
    style G fill:#fff9c4
    style I fill:#fff9c4
```

---

## Diagram 5: Employee Offboarding Workflow (Automated)

```mermaid
graph TD
    A["Employee terminated<br/>in Azure HR system"]
    B["HR system updates<br/>Entra ID"]
    C["Trigger: Employee<br/>offboarding workflow"]
    
    D["Query CyberArk for<br/>owned service principals"]
    E["Query Key Vault for<br/>assigned roles"]
    F["Query SQL for<br/>database access"]
    
    G["Revoke Entra ID<br/>role assignments"]
    H["Delete service principal<br/>certificate from CyberArk"]
    I["Rotate all database<br/>passwords"]
    J["Delete Key Vault<br/>access policies"]
    
    K["Log all actions<br/>to audit trail"]
    L["Send confirmation<br/>email to security team"]
    M["Mark employee as<br/>offboarded in CyberArk"]
    
    A --> B
    B --> C
    C --> D
    C --> E
    C --> F
    
    D --> G
    E --> J
    F --> I
    
    G --> H
    H --> I
    I --> K
    
    K --> L
    L --> M
    
    style A fill:#ffccbc
    style M fill:#c8e6c9
```

---

## Diagram 6: Real-Time Alert & Remediation Flow

```mermaid
graph TB
    A["Anomalous event detected<br/>(e.g., 5 failed auth attempts<br/>from external IP)"]
    
    B["CyberArk alert triggers"]
    C["Azure Monitor alert triggers"]
    D["Events correlated in SIEM"]
    
    E["Automated Response:<br/>Rotate suspected key immediately"]
    F["Updated secret synced to Key Vault"]
    
    G["Alert sent to Security Team<br/>via Slack/Email"]
    H["Incident ticket auto-created<br/>in Jira"]
    
    I["Security analyst investigates<br/>CloudTrail & CyberArk logs"]
    J["Confirm if compromise occurred"]
    
    K["If compromised:<br/>Revoke service principal"]
    L["Force re-auth for all dependent apps"]
    
    M["Incident closed<br/>+ Lessons learned documented"]
    
    A --> B
    A --> C
    B --> D
    C --> D
    
    D --> E
    E --> F
    F --> G
    
    G --> H
    H --> I
    I --> J
    
    J -->|Confirmed compromised| K
    K --> L
    L --> M
    
    style A fill:#ffcdd2
    style E fill:#fff9c4
    style M fill:#c8e6c9
```

---

## Diagram 7: Application Integration Options (Managed Identity vs. CyberArk API)

```mermaid
graph LR
    subgraph AzureApps["Azure-Native Applications"]
        APP1["Azure App Service"]
        FUNC["Azure Functions"]
        ACI["Container Instances"]
    end
    
    subgraph HybridApps["On-Premises / Hybrid Applications"]
        ON1["On-Premises Web Service"]
        ON2["Kubernetes Cluster"]
        ON3["Third-Party SaaS"]
    end
    
    subgraph Auth1["Authentication Method 1:<br/>Managed Identity"]
        MI1["System-Assigned MI"]
        MI2["DefaultAzureCredential"]
        MI1 --> MI2
    end
    
    subgraph Auth2["Authentication Method 2:<br/>CyberArk Certificate"]
        CERT["Client Certificate"]
        CYAPI["CyberArk REST API"]
        CERT --> CYAPI
    end
    
    subgraph Storage["Secret Storage"]
        KV["Azure Key Vault"]
        CA["CyberArk Vault"]
    end
    
    AzureApps --> Auth1
    HybridApps --> Auth2
    
    AUTH1 --> KV
    Auth2 --> CA
    
    KV -->|Synced from| CA
    
    style Auth1 fill:#c8e6c9
    style Auth2 fill:#bbdefb
```

---

## Diagram 8: Multi-Layer Security Controls

```mermaid
graph TB
    subgraph Layer1["Layer 1: Identity & Authentication"]
        direction LR
        LA["Azure Entra ID"]
        LB["Certificate-based auth"]
        LB -->|Enforced| LA
    end
    
    subgraph Layer2["Layer 2: Access Control"]
        direction LR
        LC["Conditional Access"]
        LD["MFA requirement"]
        LE["Network restrictions"]
        LC --> LD
        LC --> LE
    end
    
    subgraph Layer3["Layer 3: Vault & Secrets"]
        direction LR
        LF["CyberArk (centralized)"]
        LG["Key Vault (synced)"]
        LH["Automatic rotation"]
        LF --> LG
        LF --> LH
    end
    
    subgraph Layer4["Layer 4: Application Access"]
        direction LR
        LI["Managed identities"]
        LJ["Role-based access"]
        LK["Minimal permissions"]
        LI --> LJ
        LJ --> LK
    end
    
    subgraph Layer5["Layer 5: Monitoring & Response"]
        direction LR
        LL["Real-time alerts"]
        LM["Automated key rotation"]
        LN["Incident response"]
        LL --> LM
        LM --> LN
    end
    
    Layer1 --> Layer2
    Layer2 --> Layer3
    Layer3 --> Layer4
    Layer4 --> Layer5
    
    style Layer1 fill:#f3e5f5
    style Layer2 fill:#e1f5fe
    style Layer3 fill:#f1f8e9
    style Layer4 fill:#fff3e0
    style Layer5 fill:#fce4ec
```

---

Use these diagrams in architecture reviews, security audits, and compliance presentations to communicate the integrated control structure and demonstrate how the architecture prevents incidents like the contractor data exfiltration scenario.
