from ..clients import localstack_client


class SecurityGroupRemediator:
    def __init__(self, endpoint_url: str, region_name: str = "us-east-1"):
        self.client = localstack_client("ec2", endpoint_url, region_name)

    def remove_open_ingress(self, security_group_id: str) -> None:
        group = self.client.describe_security_groups(GroupIds=[security_group_id])["SecurityGroups"][0]
        revoke_permissions = []

        for rule in group.get("IpPermissions", []):
            if self._is_open_ssh_or_rdp(rule):
                revoke_permissions.append(rule)

        if revoke_permissions:
            self.client.revoke_security_group_ingress(GroupId=security_group_id, IpPermissions=revoke_permissions)

    def _is_open_ssh_or_rdp(self, rule: dict) -> bool:
        if any(ip_range.get("CidrIp") == "0.0.0.0/0" for ip_range in rule.get("IpRanges", [])):
            from_port = rule.get("FromPort")
            to_port = rule.get("ToPort")
            return from_port in (22, 3389) or to_port in (22, 3389)
        return False
