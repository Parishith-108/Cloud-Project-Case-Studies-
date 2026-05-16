# Architecture Decision

## Decision summary

Recommend an AWS-focused key lifecycle process that rotates AWS KMS CMKs and IAM access keys, with updated secrets stored in CyberArk.

## Decision details

- Create a new AWS KMS customer-managed key and assign a stable alias for application use.
- Rotate IAM service account access keys and create new access key pairs.
- Store the new IAM access keys securely in CyberArk and manage access through vault policies.
- Link the AWS KMS key rotation with IAM access key rotation as part of the same operational workflow.
- Keep the old KMS material and IAM keys available until validation completes, then retire them.

## Why this approach

- AWS KMS and IAM access keys are both part of the same AWS security boundary and should be managed together.
- CyberArk provides a secure vault for IAM access keys and a central place to track rotation events.
- A controlled creation and rotation sequence reduces the risk of breaking service authentication.
- Validation before retirement ensures no workloads remain tied to old key material.
