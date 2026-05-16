# AWS KMS and IAM Access Key Rotation Workflow

This workflow describes the practical steps to rotate AWS KMS keys and IAM access keys, with CyberArk as the central vault.

## 1. Detect and validate

- Identify the expired or stale AWS KMS key material.
- Identify IAM service accounts with access keys that are due for rotation.
- Capture a dependency inventory for both encryption and authentication keys.
- Confirm which workloads and services use the KMS key and IAM access keys.

## 2. Create the new KMS key

- Create a new AWS KMS customer-managed key (CMK).
- Assign a stable, reusable alias such as `alias/app-secrets-encryption`.
- Apply a KMS key policy that limits access to required roles and service principals.

## 3. Rotate IAM access keys

- Create new IAM access key pairs for the affected service accounts.
- Store the new access key ID and secret securely in CyberArk.
- Update service configuration to use the new credentials from CyberArk.

## 4. Update workload references

- Update application and infrastructure configuration to use the new KMS alias.
- Ensure service accounts retrieve IAM access keys from CyberArk rather than hard-coding secrets.
- Validate that workloads are successfully using the new key material.

## 5. Validate and monitor

- Test encryption and decryption flows using the new KMS key.
- Test service authentication using the rotated IAM access keys.
- Monitor application logs and AWS CloudTrail for any access failures.
- Confirm no services are still using old key material.

## 6. Retire old keys

- Keep the old KMS key and IAM access keys available until validation is complete.
- Retire the old KMS key and delete the old IAM access keys once the new keys are confirmed.
- Document the rotation event and update the AWS key lifecycle playbook.
