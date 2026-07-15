from dataclasses import dataclass
from typing import Protocol

from .mail.models import ParsedMail
from .models import Policy


class IntegrationUnavailable(RuntimeError):
    pass


class SharePointPolicySource(Protocol):
    def list_policies(self) -> list[Policy]: ...


class OutlookMailbox(Protocol):
    def unread_messages(self) -> list[ParsedMail]: ...


class JiraGateway(Protocol):
    def create_ticket(self, summary: str, description: str) -> str: ...


@dataclass
class LocalPolicySource:
    policies: list[Policy]

    def list_policies(self) -> list[Policy]:
        return list(self.policies)


class MicrosoftGraphSharePointSource:
    def __init__(self, site_id: str | None = None, drive_id: str | None = None) -> None:
        self.site_id = site_id
        self.drive_id = drive_id

    def list_policies(self) -> list[Policy]:
        raise IntegrationUnavailable("SharePoint Graph access is not configured")


class SimulatedOutlookMailbox:
    def __init__(self, messages: list[ParsedMail] | None = None) -> None:
        self.messages = messages or []

    def unread_messages(self) -> list[ParsedMail]:
        return list(self.messages)


class SimulatedJiraGateway:
    def __init__(self) -> None:
        self.tickets: list[dict[str, str]] = []

    def create_ticket(self, summary: str, description: str) -> str:
        key = f"SIM-{len(self.tickets) + 1}"
        self.tickets.append({"key": key, "summary": summary, "description": description})
        return key
