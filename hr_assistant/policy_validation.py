from datetime import date

from .models import Policy


def policy_issues(policy: Policy, today: date | None = None) -> tuple[str, ...]:
    today = today or date.today()
    issues = []
    if policy.owner == "unassigned":
        issues.append("missing_owner")
    if not policy.language:
        issues.append("missing_language")
    if policy.valid_until and date.fromisoformat(policy.valid_until) < today:
        issues.append("expired")
    if not policy.allowed_groups:
        issues.append("missing_access_groups")
    return tuple(issues)
