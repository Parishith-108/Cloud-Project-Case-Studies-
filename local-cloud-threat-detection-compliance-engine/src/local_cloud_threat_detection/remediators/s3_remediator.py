from ..clients import localstack_client


class S3Remediator:
    def __init__(self, endpoint_url: str, region_name: str = "us-east-1"):
        self.client = localstack_client("s3", endpoint_url, region_name)

    def enforce_bucket_controls(self, bucket_name: str) -> None:
        self.client.put_public_access_block(
            Bucket=bucket_name,
            PublicAccessBlockConfiguration={
                "BlockPublicAcls": True,
                "IgnorePublicAcls": True,
                "BlockPublicPolicy": True,
                "RestrictPublicBuckets": True,
            },
        )
        self.client.put_bucket_encryption(
            Bucket=bucket_name,
            ServerSideEncryptionConfiguration={
                "Rules": [
                    {
                        "ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "AES256"}
                    }
                ]
            },
        )
