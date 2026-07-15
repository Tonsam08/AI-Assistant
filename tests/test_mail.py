from hr_assistant.mail.cleaner import clean_mail_body
from hr_assistant.mail.parser import parse_email, to_clean_request


def test_html_mail_is_cleaned_and_attachment_is_listed():
    raw = b"""From: employee@example.test
To: hr@example.test
Subject: Leave request
Message-ID: <demo-1>
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary=x

--x
Content-Type: text/html; charset=utf-8

<p>Hello HR,</p><p>I need annual leave.</p><script>bad()</script>
--x
Content-Type: application/pdf
Content-Disposition: attachment; filename=proof.pdf
Content-Transfer-Encoding: base64

ZmljdGl2ZQ==
--x--
"""
    parsed = parse_email(raw)
    request = to_clean_request(parsed)
    assert "Hello HR" in request.text
    assert "bad()" not in request.text
    assert request.attachments[0].filename == "proof.pdf"


def test_reply_history_is_removed():
    cleaned = clean_mail_body("Current request\n\n-----Original Message-----\nOld content")
    assert cleaned == "Current request"
