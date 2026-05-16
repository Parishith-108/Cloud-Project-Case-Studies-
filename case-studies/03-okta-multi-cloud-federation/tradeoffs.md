# Tradeoffs

## Considered options

### Option 1: Centralized Okta federation for AWS and Azure
- Chosen because it provides a consistent identity control plane and simplifies auditing.
- Required effort to align cloud roles and groups, but reduced long-term operational risk.

### Option 2: Keep native cloud identity federation and separate policies
- Rejected because governance would remain fragmented and the operational burden would grow.
- AWS and Azure policies would need ongoing synchronization and duplicate enforcement.

### Option 3: Migrate to Azure AD as the primary IdP and keep Okta for provisioning
- Rejected because it would disrupt existing Okta workflows and reduce the current investment in Okta.
- Okta was already the business-wide source of truth for users and group membership.

## Tradeoff analysis

- Consistency vs. migration effort: standardizing on Okta took more upfront work, but eliminated the complexity of managing two identity planes.
- Security vs. flexibility: centralized policies can feel stricter, but they deliver stronger protection across both clouds.
- Automation vs. manual control: automated provisioning reduces stale access, while manual IAM changes are more error-prone.
- Visibility vs. trust boundaries: federating through Okta improves visibility, but each cloud account still needs careful trust configuration.
