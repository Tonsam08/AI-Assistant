import json
from pathlib import Path

from .models import Policy, UserContext


def load_policies(path: Path) -> list[Policy]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [
        Policy(
            policy_id=item["policy_id"],
            title=item["title"],
            country=item["country"],
            allowed_groups=frozenset(item["allowed_groups"]),
            content=item["content"],
            language=item.get("language", "en"),
            owner=item.get("owner", "unassigned"),
            valid_until=item.get("valid_until"),
            sensitive=item.get("sensitive", False),
            external_ai_allowed=item.get("external_ai_allowed", False),
        )
        for item in payload
    ]


def accessible_policies(policies: list[Policy], user: UserContext) -> list[Policy]:
    return [
        policy for policy in policies
        if policy.country in {user.country, "GLOBAL"}
        and (not policy.allowed_groups or policy.allowed_groups & user.groups)
        and not policy.sensitive
    ]
