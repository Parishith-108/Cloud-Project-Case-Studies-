from ..clients import localstack_client


class SecurityGroupScanner:
    def __init__(self, endpoint_url: str, region_name: str = "us-east-1"):
        self.client = localstack_client("ec2", endpoint_url, region_name)

    def audit(self) -> list[dict]:
        findings = []
        groups = self.client.describe_security_groups().get("SecurityGroups", [])

        for group in groups:
            group_id = group.get("GroupId")
            group_name = group.get("GroupName")
            for rule in group.get("IpPermissions", []):
                if self._is_open_ssh_or_rdp(rule):
                    findings.append(
                        {
                            "resource_type": "security_group",
                            "resource_id": group_id,
                            "issue": f"{group_name} allows open ingress to 0.0.0.0/0 on port {rule.get('FromPort')}",
                            "suggested_fix": "Tighten ingress rules to trusted CIDRs or remove SSH/RDP exposure.",
                        }
                    )
        return findings

    def _is_open_ssh_or_rdp(self, rule: dict) -> bool:
        from_port = rule.get("FromPort")
        to_port = rule.get("ToPort")
        ip_ranges = rule.get("IpRanges", [])
        if ip_ranges and any(ip_range.get("CidrIp") == "0.0.0.0/0" for ip_range in ip_ranges):
            if from_port in (22, 3389) or to_port in (22, 3389):
                return True
        return False
