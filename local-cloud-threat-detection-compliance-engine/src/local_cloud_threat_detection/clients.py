import boto3


def localstack_client(service_name: str, endpoint_url: str, region_name: str = "us-east-1"):
    return boto3.client(
        service_name,
        endpoint_url=endpoint_url,
        aws_access_key_id="test",
        aws_secret_access_key="test",
        region_name=region_name,
    )
