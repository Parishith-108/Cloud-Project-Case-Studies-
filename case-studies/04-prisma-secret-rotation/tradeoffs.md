# Tradeoffs

## Considered options

### Option 1: Rotate Prisma secret and update connectors
- Chosen because it addresses the expired credential directly and keeps Prisma-specific behavior isolated.
- Requires coordination with Prisma administrators and integration owners.

### Option 2: Treat Prisma rotation as part of broader cloud key rotation
- Rejected because Prisma uses its own secret model, not cloud-native key management.
- Combining it with AWS/Azure key rotation would obscure the specific Prisma workflow.

### Option 3: Delay rotation and use temporary fallback credentials
- Rejected because it increases the risk of credential drift and unauthorized access.
- A temporary workaround would leave the lifecycle gap unresolved.

## Tradeoff analysis

- Specificity vs. simplicity: a Prisma-specific rotation is more work, but it avoids assumptions about cloud key handling.
- Centralization vs. independence: CyberArk centralizes the secret, while Prisma-specific steps preserve the platform’s own integration requirements.
- Validation vs. speed: taking time to validate Prisma workflows reduces the risk of policy enforcement outages.
