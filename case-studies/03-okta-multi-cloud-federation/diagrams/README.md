# Okta Identity Federation Diagrams

This folder contains diagrams for the Okta multi-cloud federation workflow.

## Diagram

```mermaid
flowchart TD
    A[Assess current Okta, AWS, and Azure federation state] --> B[Define standard group-to-role mappings]
    B --> C[Configure Okta integration with AWS SSO / IAM Identity Center]
    B --> D[Configure Okta federation with Azure AD]
    C --> E[Apply centralized Okta conditional access policies]
    D --> E
    E --> F[Automate provisioning and lifecycle actions]
    F --> G[Validate login flows and review access mappings]
    G --> H[Maintain ongoing audit and governance]
```

Use this diagram to show the logical flow from assessment to ongoing governance.
