from pathlib import Path

from hr_assistant.models import Decision, UserContext
from hr_assistant.policies import accessible_policies, load_policies
from hr_assistant.retriever import ChromaRetriever, LocalRetriever
from hr_assistant.workflow import process_request


POLICIES = load_policies(Path("data/policies.json"))
EMPLOYEE = UserContext("u1", "FR", frozenset({"employees"}))


def test_sensitive_request_is_escalated_without_search():
    result = process_request(
        "Je veux signaler un harcèlement",
        EMPLOYEE,
        POLICIES,
        LocalRetriever(),
    )
    assert result.decision is Decision.ESCALATE
    assert result.classification.sensitive is True
    assert result.sources == ()


def test_unknown_request_asks_for_information():
    result = process_request("J’ai une question", EMPLOYEE, POLICIES, LocalRetriever())
    assert result.decision is Decision.REQUEST_INFO


def test_leave_request_returns_reviewable_answer_with_source():
    result = process_request(
        "Comment déposer une demande de congés et partir en vacances ?",
        EMPLOYEE,
        POLICIES,
        LocalRetriever(),
    )
    assert result.decision is Decision.ANSWER
    assert result.sources
    assert result.sources[0].policy.policy_id == "fr-leave-001"
    assert "validée par les RH" in result.message


def test_document_access_is_filtered_before_retrieval():
    allowed = accessible_policies(POLICIES, EMPLOYEE)
    ids = {policy.policy_id for policy in allowed}
    assert "fr-payroll-hr-001" not in ids
    assert "fr-leave-001" in ids


def test_country_access_is_enforced():
    german_user = UserContext("u2", "DE", frozenset({"employees"}))
    allowed = accessible_policies(POLICIES, german_user)
    assert {policy.policy_id for policy in allowed} == {"global-benefits-001"}


def test_chroma_retrieval_respects_pre_filtered_scope():
    allowed = accessible_policies(POLICIES, EMPLOYEE)
    results = ChromaRetriever().search("demande de congés vacances", allowed)
    assert results
    assert all(item.policy.policy_id != "fr-payroll-hr-001" for item in results)
