import pytest

from hr_assistant.connectors import (
    IntegrationUnavailable, MicrosoftGraphSharePointSource,
    SimulatedJiraGateway, SimulatedOutlookMailbox,
)


def test_unconfigured_sharepoint_fails_explicitly():
    with pytest.raises(IntegrationUnavailable):
        MicrosoftGraphSharePointSource().list_policies()


def test_simulated_jira_is_traceable():
    gateway = SimulatedJiraGateway()
    assert gateway.create_ticket("Review request", "Fictive case") == "SIM-1"
    assert gateway.tickets[0]["summary"] == "Review request"


def test_simulated_outlook_returns_configured_messages():
    assert SimulatedOutlookMailbox().unread_messages() == []
