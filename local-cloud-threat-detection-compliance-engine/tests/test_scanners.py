from unittest.mock import MagicMock, patch

from local_cloud_threat_detection.scanners.iam_scanner import IAMScanner
from local_cloud_threat_detection.scanners.s3_scanner import S3Scanner
from local_cloud_threat_detection.scanners.security_group_scanner import SecurityGroupScanner


@patch("local_cloud_threat_detection.clients.boto3.client")
def test_s3_scanner_detects_insecure_bucket(mock_client):
    mock_s3 = MagicMock()
    mock_s3.list_buckets.return_value = {"Buckets": [{"Name": "open-bucket"}]}
    mock_s3.get_public_access_block.side_effect = Exception("No access block")
    mock_s3.get_bucket_encryption.side_effect = Exception("No encryption")
    mock_client.return_value = mock_s3

    scanner = S3Scanner("http://localhost:4566")
    findings = scanner.audit()

    assert any(f["issue"] == "missing public access block" for f in findings)
    assert any(f["issue"] == "missing server-side encryption" for f in findings)


@patch("local_cloud_threat_detection.clients.boto3.client")
def test_security_group_scanner_detects_open_ingress(mock_client):
    mock_ec2 = MagicMock()
    mock_ec2.describe_security_groups.return_value = {
        "SecurityGroups": [
            {
                "GroupId": "sg-12345",
                "GroupName": "open-sg",
                "IpPermissions": [
                    {
                        "FromPort": 22,
                        "ToPort": 22,
                        "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
                    }
                ],
            }
        ]
    }
    mock_client.return_value = mock_ec2

    scanner = SecurityGroupScanner("http://localhost:4566")
    findings = scanner.audit()

    assert len(findings) == 1
    assert findings[0]["resource_type"] == "security_group"


@patch("local_cloud_threat_detection.clients.boto3.client")
def test_iam_scanner_detects_wildcard_inline_policy(mock_client):
    mock_iam = MagicMock()
    mock_iam.list_users.return_value = {"Users": [{"UserName": "test-user"}]}
    mock_iam.list_user_policies.return_value = {"PolicyNames": ["admin-policy"]}
    mock_iam.get_user_policy.return_value = {
        "PolicyDocument": {
            "Statement": [
                {
                    "Action": "*",
                    "Resource": "*",
                    "Effect": "Allow",
                }
            ]
        }
    }
    mock_client.return_value = mock_iam

    scanner = IAMScanner("http://localhost:4566")
    findings = scanner.audit()

    assert len(findings) == 1
    assert findings[0]["resource_type"] == "iam"
