from botocore.exceptions import ClientError

from ..clients import localstack_client


class S3Scanner:
    def __init__(self, endpoint_url: str, region_name: str = "us-east-1"):
        self.client = localstack_client("s3", endpoint_url, region_name)

    def audit(self) -> list[dict]:
        findings = []
        buckets = self.client.list_buckets().get("Buckets", [])

        for bucket in buckets:
            bucket_name = bucket["Name"]
            if not self._has_public_access_block(bucket_name):
                findings.append(
                    {
                        "resource_type": "s3",
                        "resource_id": bucket_name,
                        "issue": "missing public access block",
                        "suggested_fix": "Enable S3 Block Public Access and restrict public ACLs.",
                    }
                )

            if not self._has_bucket_encryption(bucket_name):
                findings.append(
                    {
                        "resource_type": "s3",
                        "resource_id": bucket_name,
                        "issue": "missing server-side encryption",
                        "suggested_fix": "Enable default bucket encryption with AES256 or AWS-managed KMS.",
                    }
                )

        return findings

    def _has_public_access_block(self, bucket_name: str) -> bool:
        try:
            response = self.client.get_public_access_block(Bucket=bucket_name)
            config = response["PublicAccessBlockConfiguration"]
            return config.get("BlockPublicAcls", False) and config.get("BlockPublicPolicy", False)
        except Exception:
            return False

    def _has_bucket_encryption(self, bucket_name: str) -> bool:
        try:
            self.client.get_bucket_encryption(Bucket=bucket_name)
            return True
        except Exception:
            return False
