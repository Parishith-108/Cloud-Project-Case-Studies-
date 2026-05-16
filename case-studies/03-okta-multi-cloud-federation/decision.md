# Architecture Decision

## Decision summary

Recommend a standardized Okta identity federation architecture for AWS and Azure that centralizes authentication, simplifies access controls, and improves auditability.

## Decision details

- Use Okta as the single source of truth for users and group membership.
- Integrate AWS SSO / AWS IAM Identity Center with Okta for AWS account access.
- Configure Azure AD federation with Okta using SAML/OIDC for Azure resource access.
- Standardize role-to-group mappings and naming conventions across both clouds.
- Enforce centralized conditional access policies in Okta for MFA, device posture, and risk-based access.
- Automate onboarding and offboarding through Okta provisioning into cloud identity sources.

## Why this approach

- A single federated identity layer reduces user friction and duplicated controls.
- Centralized policies in Okta make MFA and session controls consistent.
- Role-to-group mappings simplify entitlement reviews and reduce manual IAM changes in each cloud.
- Automating provisioning lowers the risk of orphaned accounts and stale access.
