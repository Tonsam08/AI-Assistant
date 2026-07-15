import re


INJECTION_PATTERNS = (
    r"ignore (all |the )?previous instructions",
    r"system prompt",
    r"developer message",
    r"reveal .*secret",
    r"execute (this |the )?command",
)


def contains_prompt_injection(text: str) -> bool:
    lowered = text.lower()
    return any(re.search(pattern, lowered) for pattern in INJECTION_PATTERNS)


def redact_basic_pii(text: str) -> str:
    text = re.sub(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", "[EMAIL]", text)
    return re.sub(r"(?<!\w)(?:\+?\d[\d .-]{7,}\d)(?!\w)", "[PHONE]", text)
