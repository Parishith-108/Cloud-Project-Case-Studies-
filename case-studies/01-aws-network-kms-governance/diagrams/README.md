# Architecture Diagram

This diagram shows the AWS account structure and the separate control requirements for each account. The ENI deletion protection and IAM/KMS governance flows are shown independently so the actions are not combined into a single step.

## Diagram

```mermaid
flowchart TD
  subgraph Org[AWS Organization]
    direction TB
    Sec[Security Account]
    Net[Network/Transit Account]
    App[Application Account]
    Log[Logging/Audit Account]
  end

  subgraph Security[Security Account]
    direction LR
    SA1[Guardrail policy validation]
    SA2[Permission boundary enforcement]
    SA3[Cross-account IAM role templates]
  end

  subgraph Transit[Network/Transit Account]
    direction LR
    TA1[Transit Gateway ENI protection]
    TA2[Lambda check for ENI deletion]
    TA3[Transit route dependency review]
  end

  subgraph Application[Application Account]
    direction LR
    AA1[KMS alias segregation]
    AA2[Resource-level IAM access]
    AA3[Separate key rotation approvals]
  end

  subgraph Audit[Logging/Audit Account]
    direction LR
    LA1[CloudTrail & Config capture]
    LA2[Security event aggregation]
  end

  Sec -->|Validates| SA1
  Sec -->|Applies| SA2
  Sec -->|Publishes| SA3

  Net -->|Protects| TA1
  Net -->|Checks| TA2
  Net -->|Reviews| TA3

  App -->|Manages| AA1
  App -->|Controls| AA2
  App -->|Rotates| AA3

  Log -->|Collects| LA1
  Log -->|Aggregates| LA2

  SA1 --> LA1
  TA2 --> LA1
  AA3 --> LA1

  TA1 --- TA2
  AA1 --- AA2
```

Use this diagram to show each account’s requirements separately, instead of combining ENI deletion control and IAM/KMS governance in one shared workflow.
