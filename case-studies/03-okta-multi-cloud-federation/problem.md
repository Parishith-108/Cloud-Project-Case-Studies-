# Problem Statement

## Client environment

A multi-cloud enterprise used AWS and Azure resources while Okta served as the central identity provider. The environment had grown organically, and federation was only partially implemented, which left users and administrators dealing with inconsistent access patterns.

## Observed risk

- Users had separate sign-in experiences for AWS and Azure, increasing help desk tickets and login friction.
- Okta SAML and OIDC setups were not aligned, which meant some workloads bypassed centralized policy enforcement.
- Several service principals and trust roles were granted broad access to keep integrations working.
- There was no clear governance model for federated access, so onboarding and offboarding were inconsistent.

## Business impact

If ignored, these gaps could cause:

- privilege creep across cloud environments,
- gaps in access logging and auditing,
- slow termination of departed users,
- and inconsistent enforcement of conditional access.
