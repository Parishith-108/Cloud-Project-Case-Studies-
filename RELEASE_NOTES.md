# Release Notes

## 2026-08-08

### Added

- `devsecops-iac-security-pipeline/`
  - Terraform infrastructure-as-code sample with secure and intentionally insecure AWS configurations.
  - GitHub Actions workflow for static IaC security scanning using Checkov and Trivy.
  - Example public S3 misconfiguration, open SSH/RDP security groups, and secure alternatives.
- `local-cloud-threat-detection-compliance-engine/`
  - Python-based LocalStack threat detection and compliance engine.
  - Docker Compose LocalStack setup for local AWS emulation.
  - Scanner and remediation logic for S3, EC2 security groups, and IAM misconfigurations.
  - GitHub Actions CI workflow for LocalStack integration tests and `pytest` validation.

### Updated

- Root `README.md` summary to include the new portfolio projects and CI workflows.
