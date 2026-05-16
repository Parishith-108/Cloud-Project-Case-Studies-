# Prisma Secret Rotation Workflow

This workflow describes the practical steps to rotate a Prisma-managed secret and keep CyberArk as the central vault.

## 1. Detect and validate

- Identify the expired Prisma secret and confirm which connectors and workflows depend on it.
- Review Prisma integration settings and CyberArk vault references.
- Document the dependency inventory before making changes.

## 2. Generate the new secret

- Create the new Prisma credential or API token according to Prisma’s secret management process.
- Ensure the new secret aligns with existing access policies and scopes.

## 3. Update Prisma integrations

- Update Prisma connectors, integrations, and automation tools to use the new secret.
- Test the updated connections in a controlled environment.

## 4. Sync with CyberArk

- Store the rotated Prisma secret in CyberArk.
- Update vault policies and access controls for the new credential.
- Preserve the old secret in CyberArk until validation is complete.

## 5. Validate and retire

- Validate Prisma workflows, policy scans, and automation operations.
- Monitor for authentication issues and connector failures.
- Retire the old secret once the rotation is confirmed successful.
- Document the rotation and add the process to the secret lifecycle playbook.
