# Architecture Decision

## Decision summary

Recommend a Prisma-specific secret rotation process that creates new Prisma credentials, updates connector configurations, and stores the updated secret in CyberArk.

## Decision details

- Rotate the Prisma-managed secret used by policy enforcement and automation workflows.
- Update all Prisma connectors and integrations to use the new credential.
- Store the new secret in CyberArk and manage access through the existing vault policy.
- Keep the old secret available during validation, then retire it once all Prisma workflows are confirmed healthy.

## Why this approach

- Prisma has its own secret and integration model, so treating it separately avoids cloud key assumptions.
- CyberArk remains the central control point for credential management and access.
- A controlled rotation with validation minimizes disruption to policy enforcement.
- Documenting the Prisma-specific process closes a gap in the overall key lifecycle.
