import html
import re


def html_to_text(value: str) -> str:
    value = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", value, flags=re.I | re.S)
    value = re.sub(r"<br\s*/?>|</p>|</div>", "\n", value, flags=re.I)
    value = re.sub(r"<[^>]+>", " ", value)
    value = html.unescape(value)
    lines = [re.sub(r"\s+", " ", line).strip() for line in value.splitlines()]
    return "\n".join(line for line in lines if line)


def remove_reply_history(value: str) -> str:
    markers = ("-----Original Message-----", "De :", "From:", "On ")
    positions = [value.find(marker) for marker in markers if value.find(marker) >= 0]
    return value[: min(positions)].strip() if positions else value.strip()


def clean_mail_body(value: str, is_html: bool = False) -> str:
    cleaned = html_to_text(value) if is_html else value
    cleaned = remove_reply_history(cleaned)
    return re.sub(r"\n{3,}", "\n\n", cleaned).strip()
