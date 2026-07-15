import hashlib
import math
import re
from collections import defaultdict
from collections.abc import Iterable

from .models import Classification


TRAINING_EXAMPLES = {
    "leave": [
        "demande de congés vacances absence", "annual leave holiday request",
        "Urlaub Abwesenheit beantragen", "solicitud de vacaciones permiso",
    ],
    "remote_work": [
        "télétravail travail à distance", "remote work home office",
        "Homeoffice Telearbeit", "trabajo remoto desde casa",
    ],
    "payroll": [
        "salaire paie bulletin cotisation", "salary payroll payslip",
        "Gehalt Lohnabrechnung", "salario nómina",
    ],
    "benefits": [
        "transport mutuelle avantages remboursement", "benefits reimbursement insurance",
        "Leistungen Erstattung Versicherung", "beneficios reembolso seguro",
    ],
}

SENSITIVE_TERMS = {
    "harcèlement", "harcelement", "harassment", "discrimination", "maladie",
    "médical", "medical", "licenciement", "dismissal", "sanction", "grossesse",
    "pregnancy", "handicap", "disability", "termination", "grievance",
}

STOPWORDS = {
    "a", "à", "and", "au", "aux", "avec", "can", "comment", "de", "des", "do",
    "du", "en", "et", "how", "i", "ich", "je", "la", "le", "les", "me", "mein",
    "meine", "mon", "my", "need", "necesito", "para", "prendre", "request", "report",
    "souhaite", "the", "to", "un", "une", "want", "with",
}


def _tokens(text: str) -> list[str]:
    return [
        token for token in re.findall(r"[\wÀ-ÿ'-]+", text.lower())
        if token not in STOPWORDS
    ]


class HashingEmbeddingProvider:
    """Backend local reproductible. À remplacer par l'embedding approuvé en production."""

    def __init__(self, dimensions: int = 2048) -> None:
        self.dimensions = dimensions

    def embed(self, text: str) -> list[float]:
        vector = [0.0] * self.dimensions
        for token in _tokens(text):
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], "big") % self.dimensions
            vector[index] += 1.0
        norm = math.sqrt(sum(value * value for value in vector)) or 1.0
        return [value / norm for value in vector]


def _cosine(left: Iterable[float], right: Iterable[float]) -> float:
    return sum(a * b for a, b in zip(left, right))


class EmbeddingClassifier:
    def __init__(self, provider=None, examples=None) -> None:
        self.provider = provider or HashingEmbeddingProvider()
        self.examples = examples or TRAINING_EXAMPLES
        self.topic_vectors = {
            topic: [self.provider.embed(sample) for sample in samples]
            for topic, samples in self.examples.items()
        }

    def classify(self, text: str) -> Classification:
        normalised = " ".join(_tokens(text))
        sensitive = any(term in normalised for term in SENSITIVE_TERMS)
        if not normalised:
            return Classification("unknown", sensitive, 0.0, ("topic",))

        embedded = self.provider.embed(normalised)
        scores = {
            topic: max(_cosine(embedded, vector) for vector in vectors)
            for topic, vectors in self.topic_vectors.items()
        }
        topic, score = max(scores.items(), key=lambda item: item[1])
        if score < 0.08:
            return Classification("unknown", sensitive, score, ("topic",))
        confidence = min(0.55 + score, 0.98)
        return Classification(topic, sensitive, confidence)


_DEFAULT_CLASSIFIER = EmbeddingClassifier()


def classify_request(text: str) -> Classification:
    return _DEFAULT_CLASSIFIER.classify(text)
