from datetime import date

from hr_assistant.models import Policy
from hr_assistant.policy_validation import policy_issues


def test_expired_or_unowned_policy_is_flagged():
    policy = Policy("p1", "Old", "FR", frozenset(), "Text", valid_until="2020-01-01")
    issues = policy_issues(policy, date(2026, 1, 1))
    assert {"missing_owner", "expired", "missing_access_groups"} <= set(issues)
