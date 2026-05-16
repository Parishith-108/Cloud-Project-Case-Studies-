# Tradeoffs

## Considered options

### Option 1: GitOps + drift detection for Okta-AWS role mappings (chosen)
- Provides an audit trail for all role assignment changes and prevents accidental privilege escalation.
- Catches misconfigurations within 15 minutes through automated drift detection.
- Requires infrastructure investment (Lambda, SNS, metrics) and a version-controlled repository.
- Adds latency (up to 15 minutes) between a role assignment and detection of a misconfiguration.

### Option 2: Manual peer review in Okta with no automation
- Simpler to implement; relies on human judgment at approval time.
- Rejected because the incident proved that humans can make mistakes under time pressure, and post-approval validation is missing.
- Would not have prevented the 4-hour window of undetected privilege escalation.

### Option 3: Fully manual role management with IAM as source of truth
- Rejected because it abandons Okta's value as a central identity platform.
- Would increase help desk burden and reintroduce separate AWS IAM management workflows.

### Option 4: ABAC only, eliminate static role mappings
- Provides maximum flexibility but requires all resource teams to adopt session tag-based policies.
- Rejected as a pure solution because it lacks the initial controls to prevent role misassignment in the first place.
- Adopted as a long-term complement to Option 1.

## Tradeoff analysis

- **Automation vs. flexibility**: Drift detection adds 15 minutes of delay but eliminates silent misconfigurations. The tradeoff is acceptable for production AWS accounts.
- **Audit trail vs. operational simplicity**: GitOps adds tooling complexity but provides forensic evidence of who changed what and when.
- **Centralized control vs. team autonomy**: Peer review gates on role changes restrict engineer autonomy but prevent incidents like the wrong-role-mapping scenario.
- **Immediate vs. eventual consistency**: CloudFormation or Terraform could enforce static role mappings, but GitOps + drift detection allows for rollback and human intervention if needed.
- **Cost vs. risk mitigation**: The Lambda and monitoring cost ($50–100/month) is negligible compared to the cost of a compliance violation or security incident.
