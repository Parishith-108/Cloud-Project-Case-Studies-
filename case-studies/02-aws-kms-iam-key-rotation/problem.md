# Problem Statement

## Client environment

An AWS security team discovered that key material used by their KMS encryption and IAM service accounts had become stale. Critical workloads relied on an AWS KMS customer-managed key (CMK) for encryption, while service accounts used IAM access keys that were stored and rotated through CyberArk.

## Observed risk

- A KMS key alias pointed to expired or out-of-rotation key material.
- Service workloads were using IAM access keys that were overdue for rotation.
- CyberArk contained the existing access key and secret pair, but the rotation controls were not tightly linked with AWS key lifecycle events.
- There was no formal process for creating, rotating, and retiring AWS KMS keys and IAM access keys together.

## Business impact

If left unresolved, this issue could have caused:

- application outages due to expired encryption key material,
- service failures from stale IAM access keys,
- and increased risk from unmanaged keying material in the AWS environment.
