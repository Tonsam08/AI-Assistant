from email import policy
from email.parser import BytesParser
from uuid import uuid4

from .cleaner import clean_mail_body
from .models import AttachmentMetadata, CleanRequest, ParsedMail


def parse_email(raw: bytes) -> ParsedMail:
    message = BytesParser(policy=policy.default).parsebytes(raw)
    bodies: list[str] = []
    attachments: list[AttachmentMetadata] = []
    for part in message.walk():
        if part.is_multipart():
            continue
        payload = part.get_payload(decode=True) or b""
        filename = part.get_filename()
        if filename:
            attachments.append(AttachmentMetadata(filename, part.get_content_type(), len(payload)))
        elif part.get_content_type() in {"text/plain", "text/html"}:
            charset = part.get_content_charset() or "utf-8"
            bodies.append(clean_mail_body(payload.decode(charset, errors="replace"), part.get_content_type() == "text/html"))
    return ParsedMail(
        message.get("Message-ID") or f"generated-{uuid4()}",
        message.get("From", "unknown"),
        message.get("Subject", ""),
        "\n\n".join(body for body in bodies if body),
        tuple(attachments),
    )


def to_clean_request(mail: ParsedMail) -> CleanRequest:
    return CleanRequest(mail.message_id, mail.sender, mail.subject, mail.body, mail.attachments)
