from dataclasses import dataclass


@dataclass(frozen=True)
class AttachmentMetadata:
    filename: str
    content_type: str
    size: int


@dataclass(frozen=True)
class ParsedMail:
    message_id: str
    sender: str
    subject: str
    body: str
    attachments: tuple[AttachmentMetadata, ...]


@dataclass(frozen=True)
class CleanRequest:
    request_id: str
    sender: str
    subject: str
    text: str
    attachments: tuple[AttachmentMetadata, ...]
