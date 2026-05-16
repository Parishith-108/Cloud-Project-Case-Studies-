# Prisma Secret Rotation Diagrams

This folder contains diagrams for the Prisma secret rotation workflow.

## Diagram

```mermaid
flowchart TD
    A[Expired Prisma secret detected] --> B[Inventory Prisma connectors and CyberArk references]
    B --> C[Generate new Prisma secret/token]
    C --> D[Update Prisma connectors and automation workflows]
    D --> E[Store new secret in CyberArk]
    E --> F[Validate Prisma workflows and scans]
    F --> G[Retire old Prisma secret after verification]
    G --> H[Document rotation and update playbook]
```

Use this diagram to show the Prisma-specific rotation flow with CyberArk as the central vault.
