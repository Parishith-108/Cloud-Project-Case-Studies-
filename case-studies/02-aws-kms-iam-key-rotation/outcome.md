# Outcome

## What changed

- A new AWS KMS customer-managed key was created and aliased for application use.
- IAM service account access keys were rotated and new key pairs were created.
- New IAM access keys were securely stored in CyberArk and managed through vault policies.
- Old KMS key material and old IAM access keys were retired only after successful validation.

## Results

- AWS encryption and authentication workloads stabilized.
- The security posture improved through a combined KMS and IAM key rotation process.
- CyberArk became the central means for managing and auditing AWS secrets.
- The organization gained a repeatable AWS key lifecycle playbook.
