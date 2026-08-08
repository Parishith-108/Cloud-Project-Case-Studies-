import argparse
from pathlib import Path

from .init_resources import create_mock_resources
from .output import emit_findings
from .scanners.iam_scanner import IAMScanner
from .scanners.s3_scanner import S3Scanner
from .scanners.security_group_scanner import SecurityGroupScanner
from .remediators.s3_remediator import S3Remediator
from .remediators.security_group_remediator import SecurityGroupRemediator
from .clients import localstack_client


DEFAULT_ENDPOINT = "http://localhost:4566"
DEFAULT_REPORT = Path("compliance-findings.json")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Local Cloud Threat Detection & Compliance Engine"
    )
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT, help="LocalStack endpoint URL")
    parser.add_argument("--init", action="store_true", help="Create mock insecure LocalStack resources")
    parser.add_argument("--fix", action="store_true", help="Apply remediation for detected findings")
    parser.add_argument(
        "--output",
        default=str(DEFAULT_REPORT),
        help="Path to write the compliance findings JSON report",
    )
    args = parser.parse_args()

    endpoint_url = args.endpoint
    if args.init:
        create_mock_resources(endpoint_url)
        print("Initialization complete. Run the scanner after LocalStack is ready.")
        return 0

    s3_scanner = S3Scanner(endpoint_url)
    sg_scanner = SecurityGroupScanner(endpoint_url)
    iam_scanner = IAMScanner(endpoint_url)

    findings = []
    findings.extend(s3_scanner.audit())
    findings.extend(sg_scanner.audit())
    findings.extend(iam_scanner.audit())

    if args.fix:
        s3_remediator = S3Remediator(endpoint_url)
        security_remediator = SecurityGroupRemediator(endpoint_url)

        for finding in findings:
            if finding["resource_type"] == "s3":
                s3_remediator.enforce_bucket_controls(finding["resource_id"])
            elif finding["resource_type"] == "security_group":
                security_remediator.remove_open_ingress(finding["resource_id"])

        findings = []
        findings.extend(s3_scanner.audit())
        findings.extend(sg_scanner.audit())
        findings.extend(iam_scanner.audit())

    emit_findings(findings, Path(args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
