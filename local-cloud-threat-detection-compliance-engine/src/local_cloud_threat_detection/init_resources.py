import json
from pathlib import Path

from .clients import localstack_client


DEFAULT_CONFIG_PATH = Path(__file__).resolve().parents[2] / "config" / "localstack_resources.json"


def load_config(config_path: Path | None = None) -> dict:
    path = config_path or DEFAULT_CONFIG_PATH
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def create_mock_resources(endpoint_url: str, config_path: Path | None = None) -> dict:
    config = load_config(config_path)
    region = config.get("region", "us-east-1")
    bucket_name = config["bucket_name"]
    sg_name = config["security_group_name"]
    iam_user_name = config["iam_user_name"]

    s3 = localstack_client("s3", endpoint_url, region)
    ec2 = localstack_client("ec2", endpoint_url, region)
    iam = localstack_client("iam", endpoint_url, region)

    print(f"Creating mock bucket {bucket_name} in LocalStack...")
    s3.create_bucket(Bucket=bucket_name)

    print("Creating insecure EC2 security group...")
    vpcs = ec2.describe_vpcs().get("Vpcs", [])
    if vpcs:
        vpc_id = vpcs[0]["VpcId"]
    else:
        vpc = ec2.create_vpc(CidrBlock="10.0.0.0/16")
        vpc_id = vpc["Vpc"]["VpcId"]
    sg_args = {"GroupName": sg_name, "Description": "Open SSH and RDP security group", "VpcId": vpc_id}
    security_group = ec2.create_security_group(**sg_args)
    group_id = security_group["GroupId"]

    ec2.authorize_security_group_ingress(
        GroupId=group_id,
        IpPermissions=[
            {
                "IpProtocol": "tcp",
                "FromPort": 22,
                "ToPort": 22,
                "IpRanges": [{"CidrIp": "0.0.0.0/0", "Description": "Open SSH"}],
            },
            {
                "IpProtocol": "tcp",
                "FromPort": 3389,
                "ToPort": 3389,
                "IpRanges": [{"CidrIp": "0.0.0.0/0", "Description": "Open RDP"}],
            },
        ],
    )

    print(f"Creating IAM user {iam_user_name} with overly permissive inline policy...")
    iam.create_user(UserName=iam_user_name)
    iam.put_user_policy(
        UserName=iam_user_name,
        PolicyName="localstack-privileged-inline-policy",
        PolicyDocument=json.dumps(
            {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "AllowEverything",
                        "Effect": "Allow",
                        "Action": "*",
                        "Resource": "*",
                    }
                ],
            }
        ),
    )

    return {
        "bucket_name": bucket_name,
        "security_group_name": sg_name,
        "iam_user_name": iam_user_name,
        "region": region,
        "endpoint_url": endpoint_url,
    }
