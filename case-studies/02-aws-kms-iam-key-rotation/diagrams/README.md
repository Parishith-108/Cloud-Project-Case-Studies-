# KMS Key Rotation Diagrams

This folder contains diagrams for the AWS KMS and IAM access key rotation workflow.

## Diagram

```mermaid
flowchart TD
    A[Expired AWS KMS or IAM key detected] --> B[Inventory AWS KMS dependencies and IAM service accounts]
    B --> C[Create new AWS KMS CMK and assign alias]
    B --> D[Create new IAM access key pairs]
    C --> E[Store new access keys and metadata in CyberArk]
    D --> E
    E --> F[Update workload references to CyberArk secrets and KMS alias]
    F --> G[Validate encryption and authentication flows]
    G --> H[Retire old AWS KMS key and IAM access keys]
    H --> I[Document rotation and update playbook]
```

Use this diagram to show the AWS-only key rotation flow with CyberArk as the secure vault.
