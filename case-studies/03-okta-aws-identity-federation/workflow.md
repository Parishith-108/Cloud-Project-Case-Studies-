# Okta Identity Federation Workflow

This workflow describes how to implement governed Okta-to-AWS federation with drift detection to prevent role misassignment incidents.

## 1. Audit current Okta-AWS mappings

- Export all active Okta groups and their current AWS role assignments from AWS IAM Identity Center.
- Cross-reference with CloudTrail to identify who last modified each role mapping and when.
- Create an inventory of all role-to-group mappings and document business justification for each.
- Flag any overly broad role assignments (e.g., `prod-admin` assigned to a group intended for read-only access).

## 2. Establish a source-of-truth repository

- Create a private GitHub/GitLab repository with a YAML or JSON file listing all approved Okta-group-to-AWS-role mappings.
- Use this format:
  ```yaml
  prod-database-admin:
    okta_groups:
      - platform-dba
    aws_accounts:
      - '111122223333'
    requires_mfa: true
    session_duration: 1h
  prod-application-read:
    okta_groups:
      - developers
      - qa-team
    aws_accounts:
      - '111122223333'
    requires_mfa: false
    session_duration: 8h
  ```
- Enforce require-review policy on this repository; only DevOps/Security can merge changes.

## 3. Implement drift detection

- Deploy a Lambda function that runs every 15 minutes to compare current AWS IAM Identity Center role mappings against the source-of-truth repository.
- If a discrepancy is detected (e.g., an Okta group is assigned a role not in the repo), trigger a CloudWatch alarm and log the event to a DynamoDB table.
- Send a Slack/email alert with details: which group, which role, which AWS account, and who made the change (from CloudTrail).
- Example alert: `DRIFT DETECTED: Okta group 'platform-engineering' assigned role 'prod-rds-admin' on account 111122223333 (not in source-of-truth). Changed by john.smith@company.com at 2026-05-16 14:32 UTC`.

## 4. Create role mapping change process

- When an engineer requests a new Okta group or role assignment, they submit a pull request to the source-of-truth repository.
- PR description must include: business justification, which groups/roles, which AWS accounts, and anticipated session duration.
- Two approvers (Security and a domain expert) must review and approve before merge.
- Once merged, the drift detection Lambda will reconcile the mapping within 15 minutes; no manual sync needed.
- If an off-policy change is made directly in AWS IAM Identity Center, the next drift check will revert it and alert the team.

## 5. Automate Okta-to-AWS IAM Identity Center sync

- Use AWS IAM Identity Center's native Okta SCIM integration to sync users and groups.
- Ensure Okta group naming matches the role mapping repository (e.g., group name `prod-application-read` should map to role `prod-application-read`).
- Test that adding a user to an Okta group results in the correct AWS role assignment within 5 minutes.

## 6. Enforce conditional access in Okta

- Require MFA for login to `prod-*` roles; allow passwordless for `dev-*` roles.
- Enforce Okta device trust: managed devices only for sensitive roles.
- Set session timeout: 1 hour for prod, 8 hours for dev.
- Configure risk-based authentication to prompt for step-up MFA if login velocity is anomalous.

## 7. Offboarding and access revocation

- When an employee leaves, remove them from all Okta groups.
- The SCIM integration automatically removes AWS role assignments within 5 minutes.
- Run a post-offboarding validation: query AWS CloudTrail for the departing user's last API call and verify no subsequent access attempts.

## 8. Quarterly audit and review

- Review the drift detection logs for patterns (e.g., frequent manual changes outside the change process).
- Audit the role mapping repository for roles that are no longer in use and remove them.
- Solicit feedback from teams on access friction; adjust session durations or MFA policies if needed.
- Validate that all `prod-admin` roles are assigned to exactly the intended groups.
