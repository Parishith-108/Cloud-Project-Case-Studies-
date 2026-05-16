# Problem Statement

## Client environment

A SaaS company used AWS exclusively with Okta as the central identity provider for all employee access. As the organization scaled, AWS account sprawl and role proliferation made IAM governance increasingly complex. Okta group-to-AWS-role mappings were not consistently validated, and engineers had the ability to modify federation role assignments.

## Critical incident

A platform engineer mistakenly mapped the wrong role in an Okta group during a routine access request approval. Specifically, they assigned the `prod-database-admin` role (with unrestricted RDS, Secrets Manager, and KMS access) to an Okta group intended for `prod-application-read` access. This misconfiguration remained undetected for 4 hours across 3 production AWS accounts until a CloudWatch alert triggered on unusual API calls from the affected group members.

## Observed risks

- Manual role mapping changes in Okta were not validated against AWS IAM policies or naming conventions before taking effect.
- No automated drift detection to catch when an Okta group received permissions outside its intended scope.
- Engineers had too much autonomy to modify federation mappings without peer review.
- CloudTrail and Okta logs were not correlated to identify the root cause immediately.
- Offboarding and privilege cleanup were slow due to unclear role-to-group ownership.

## Business impact

If governance remains loose, these gaps could enable:

- privilege creep where developers accumulate admin access over time,
- undetected insider threats or social engineering attacks that exploit broad permissions,
- compliance violations if auditors find unreviewed role assignments,
- and slow incident response when suspicious API activity occurs.
