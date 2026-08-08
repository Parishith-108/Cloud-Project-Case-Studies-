from botocore.exceptions import ClientError

from ..clients import localstack_client


class IAMScanner:
    def __init__(self, endpoint_url: str, region_name: str = "us-east-1"):
        self.client = localstack_client("iam", endpoint_url, region_name)

    def audit(self) -> list[dict]:
        findings = []
        users = self.client.list_users().get("Users", [])

        for user in users:
            user_name = user.get("UserName")
            inline_policies = self.client.list_user_policies(UserName=user_name).get("PolicyNames", [])
            for policy_name in inline_policies:
                policy = self.client.get_user_policy(UserName=user_name, PolicyName=policy_name)
                document = policy.get("PolicyDocument", {})
                for statement in document.get("Statement", []):
                    if self._is_overly_permissive(statement):
                        findings.append(
                            {
                                "resource_type": "iam",
                                "resource_id": user_name,
                                "issue": f"inline policy {policy_name} grants wildcard permissions",
                                "suggested_fix": "Restrict IAM actions and resources to the minimum required set.",
                            }
                        )
        return findings

    def _is_overly_permissive(self, statement: dict) -> bool:
        actions = statement.get("Action", [])
        resources = statement.get("Resource", [])
        if isinstance(actions, str):
            actions = [actions]
        if isinstance(resources, str):
            resources = [resources]

        return "*" in actions or "*" in resources
