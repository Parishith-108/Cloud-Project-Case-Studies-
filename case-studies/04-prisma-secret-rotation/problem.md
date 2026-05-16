# Problem Statement

## Client environment

A security team discovered that a Prisma-managed secret used for policy enforcement and automation workflows had expired. The secret was referenced by Prisma connectors, cloud policy integrations, and CyberArk vault entries used for secure storage.

## Observed risk

- Prisma policy enforcement agents began failing to authenticate.
- Automated security checks and configuration scans were interrupted.
- The expired secret remained in CyberArk, creating a stale dependency with the rest of the secret lifecycle.
- There was no documented Prisma-specific rotation process.

## Business impact

If left unresolved, the issue could have caused:

- gaps in security posture management,
- delayed detection of policy violations,
- and elevated risk of relying on temporary fallback credentials.
