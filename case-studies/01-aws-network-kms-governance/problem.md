# Problem Statement

## Client environment

An AWS operations team was managing a VPC topology that included critical transit gateway connections and Lambda functions that depended on dedicated ENIs. Encryption keys were managed through AWS KMS aliases, and IAM users and service roles were granted access through a combination of inline policies and role templates.

During an architecture review, the team found a gap in lifecycle governance: ENIs could be deleted without a dependency check, transit gateway attachments were not protected for Lambda-dependent paths, and KMS alias usage was not consistently enforced. At the same time, user roles and policies had grown permissive to avoid blocking operations.

## Risk

- Deleting an ENI could break the transit gateway path for Lambda-backed services.
- Transit gateway attachments were effectively a single point of failure for multi-VPC traffic.
- KMS key usage without alias enforcement increased the risk of hard-coded key IDs and accidental key rotation failures.
- IAM users and roles had overly broad permissions, which made it hard to control who could delete network resources or modify key and policy configurations.

## Business impact

If left unaddressed, these issues could cause:

- unexpected application outages from ENI removal,
- disrupted connectivity across the transit gateway,
- encryption failures from incorrect KMS key references,
- and privilege abuse from overly permissive IAM roles.
