# Architecture Decision

## Decision summary

Implement a governed Okta-to-AWS federation model where role mapping changes are validated, reviewed, and automatically monitored for drift. This prevents privilege escalation incidents like the wrong-role-mapping incident and ensures compliance with principle of least privilege.

## Decision details

- Use Okta as the single source of truth for user and group membership in AWS.
- Integrate AWS IAM Identity Center with Okta for federated AWS account access and role assignment.
- Enforce a GitOps-style role mapping repository where all Okta-to-AWS-role mappings are version-controlled and require peer review before changes.
- Deploy an automated drift detection Lambda that compares Okta group-to-role mappings against the source-of-truth repository every 15 minutes.
- Configure CloudWatch alarms to trigger when drift is detected or when a group is assigned a role outside its approval scope.
- Implement attribute-based access control (ABAC) in AWS IAM using Okta group names and session tags, reducing the need to maintain explicit role-to-group mappings.
- Enforce centralized conditional access policies in Okta for MFA, device posture, and session duration based on AWS account environment (prod vs. dev).
- Automate offboarding through Okta provisioning to AWS IAM Identity Center and validate that no residual access remains in CloudTrail.

## Why this approach

- GitOps for role mappings creates an audit trail and prevents accidental privilege escalation.
- Automated drift detection catches misconfigurations within minutes instead of hours.
- Peer review gates on role mapping changes reduce human error and insider risk.
- ABAC simplifies role sprawl by using Okta attributes instead of managing static role lists.
- Okta conditional access ensures MFA is enforced even if AWS roles are misassigned.
- Automated offboarding verification prevents orphaned access that could be exploited.
