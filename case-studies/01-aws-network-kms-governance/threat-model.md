# Threat Model

## Assets

- AWS ENIs and transit gateway attachments
- Lambda functions that depend on ENIs for network connectivity
- AWS KMS keys and aliases
- IAM users, roles, and policies
- CloudTrail logs and EventBridge alerts

## Threats

- Accidental or malicious deletion of critical ENIs
- Transit gateway reconfiguration that breaks Lambda-dependent paths
- Misuse of AWS KMS keys through direct key ID references instead of aliases
- Overly broad IAM policies allowing destructive network or KMS actions
- Compromise of user roles with permission to modify network or encryption configurations

## Controls

- Tag critical ENIs and apply IAM deny policies to prevent deletion unless explicitly approved.
- Enforce transit gateway attachment validation in deployment pipelines and alert on changes.
- Standardize KMS key usage on aliases and validate alias references in code and configuration.
- Tighten user roles and policies with least privilege, explicit denies for delete actions, and session restrictions.
- Use CloudTrail and EventBridge to detect ENI deletion attempts and unauthorized transit gateway or KMS changes.

## Validation

- Run automated checks on IAM policy changes to ensure they do not permit unauthorized ENI or transit gateway deletion.
- Review KMS alias usage in infrastructure code and runtime configurations.
- Validate Lambda network dependencies and transit gateway route stability after changes.
- Monitor for anomalous API calls involving `DeleteNetworkInterface`, transit gateway modifications, and KMS key usage.
