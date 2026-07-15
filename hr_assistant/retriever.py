import hashlib
import math
import re
from collections.abc import Iterable

from .models import Policy, SearchResult


def _tokens(text: str) -> list[str]:
    return re.findall(r"[\wÀ-ÿ'-]+", text.lower())


def _embedding(text: str, dimensions: int = 256) -> list[float]:
    """Embedding local déterministe pour la démo, sans appel externe."""
    vector = [0.0] * dimensions
    for token in _tokens(text):
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        index = int.from_bytes(digest[:4], "big") % dimensions
        vector[index] += 1.0
    norm = math.sqrt(sum(value * value for value in vector)) or 1.0
    return [value / norm for value in vector]


def _cosine(left: Iterable[float], right: Iterable[float]) -> float:
    return sum(a * b for a, b in zip(left, right))


class LocalRetriever:
    """Moteur testable. Il sera remplacé par ChromaRetriever en intégration."""

    def search(self, query: str, policies: list[Policy], limit: int = 3) -> list[SearchResult]:
        query_vector = _embedding(query)
        results = [
            SearchResult(policy, _cosine(query_vector, _embedding(f"{policy.title} {policy.content}")))
            for policy in policies
        ]
        return sorted(results, key=lambda item: item.score, reverse=True)[:limit]


class ChromaRetriever:
    """Recherche ChromaDB avec embedding local interchangeable."""

    def __init__(self) -> None:
        import chromadb

        self._client = chromadb.EphemeralClient()

    def search(self, query: str, policies: list[Policy], limit: int = 3) -> list[SearchResult]:
        if not policies:
            return []
        access_scope = hashlib.sha256(
            "|".join(sorted(policy.policy_id for policy in policies)).encode("utf-8")
        ).hexdigest()[:16]
        collection = self._client.get_or_create_collection(
            name=f"policies_{access_scope}",
            metadata={"hnsw:space": "cosine"},
        )
        current_ids = set(collection.get()["ids"])
        new_policies = [policy for policy in policies if policy.policy_id not in current_ids]
        if new_policies:
            collection.add(
                ids=[policy.policy_id for policy in new_policies],
                embeddings=[_embedding(f"{policy.title} {policy.content}") for policy in new_policies],
                documents=[policy.content for policy in new_policies],
            )
        result = collection.query(
            query_embeddings=[_embedding(query)],
            n_results=min(limit, len(policies)),
            include=["distances"],
        )
        by_id = {policy.policy_id: policy for policy in policies}
        return [
            SearchResult(by_id[policy_id], 1.0 - distance)
            for policy_id, distance in zip(result["ids"][0], result["distances"][0])
            if policy_id in by_id
        ]
