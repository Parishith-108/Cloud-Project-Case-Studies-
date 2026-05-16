# Tradeoffs

## Considered options

### Option 1: Rotate AWS KMS keys and IAM access keys together with CyberArk vault coordination
- Chosen because it aligns AWS encryption and authentication key lifecycles.
- Requires coordination between AWS KMS, IAM, and CyberArk.

### Option 2: Rotate only the KMS key and leave IAM access keys unchanged
- Rejected because stale IAM access keys would still pose an authentication risk.
- Does not fully address the key lifecycle gap for service accounts.

### Option 3: Rotate only IAM access keys and leave the KMS key unchanged
- Rejected because expired or stale KMS encryption material would continue to threaten workload availability.
- Partial rotation leaves critical encryption dependencies unaddressed.

## Tradeoff analysis

- Security vs. operational effort: rotating both KMS and IAM access keys together is more work, but it closes the overall AWS key lifecycle gap.
- Integrated workflow vs. isolated rotation: a combined process reduces the chance of mismatched rotation timing.
- Validation vs. speed: validating both key types before retirement slows the cutover, but it prevents production failures.
