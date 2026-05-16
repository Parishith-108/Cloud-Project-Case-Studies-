# Architecture Decision

## Decision summary

Recommend an AWS-focused governance model that protects ENI deletion, secures transit gateway and Lambda dependencies, enforces KMS alias usage, and tightens IAM user role and policy changes.

## Decision details

- Implement resource protection for ENIs by tagging critical network interfaces and preventing accidental deletion through IAM conditions and guardrails.
- Protect transit gateway attachments used by Lambda functions with configuration checks and dependency-aware alerts.
- Standardize AWS KMS usage on aliases instead of raw key IDs, and enforce alias references in all application and infrastructure configurations.
- Review and edit IAM user roles and policies to remove broad permissions, enforce least privilege, and add explicit deny conditions for destructive network and KMS actions.
- Use CloudWatch Events / EventBridge rules to detect ENI deletion attempts or transit gateway changes, and trigger remediation or approvals.

## Why this approach

- Protecting ENIs and transit gateway attachments prevents a single deletion from cascading into a larger outage.
- KMS aliases create a stable reference point for key rotation and reduce the risk of hard-coded key dependencies.
- Tightening IAM roles and policies reduces the attack surface and makes operational changes auditable.
- A dependency-aware governance model improves both availability and security for AWS networking and encryption.
