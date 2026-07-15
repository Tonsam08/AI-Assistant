import re

from .models import Classification


TOPICS = {
    "leave": {"congé", "conges", "vacances", "absence", "leave", "holiday"},
    "remote_work": {"télétravail", "teletravail", "remote", "home office"},
    "payroll": {"salaire", "paie", "bulletin", "cotisation", "payroll", "salary"},
    "benefits": {"transport", "mutuelle", "avantage", "benefit", "reimbursement"},
}

SENSITIVE_TERMS = {
    "harcèlement", "harcelement", "discrimination", "maladie", "médical",
    "medical", "licenciement", "sanction", "grossesse", "handicap",
}


def _normalise(text: str) -> str:
    return " ".join(re.findall(r"[\wÀ-ÿ'-]+", text.lower()))


def classify_request(text: str) -> Classification:
    normalised = _normalise(text)
    sensitive = any(term in normalised for term in SENSITIVE_TERMS)

    scores = {
        topic: sum(term in normalised for term in terms)
        for topic, terms in TOPICS.items()
    }
    topic, hits = max(scores.items(), key=lambda item: item[1])
    if hits == 0:
        return Classification("unknown", sensitive, 0.25, ("topic",))

    confidence = min(0.65 + 0.12 * (hits - 1), 0.95)
    return Classification(topic, sensitive, confidence)
