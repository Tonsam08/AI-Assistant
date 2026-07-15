import hashlib
import math
import re
from collections import defaultdict
from collections.abc import Iterable

from .chunking import chunk_policy
from .models import Policy, SearchResult


def _tokens(text: str) -> list[str]:
    return re.findall(r"[\wÀ-ÿ'-]+", text.lower())


def _local_embedding(text: str, dimensions: int = 2048) -> list[float]:
    """Secours déterministe réservé aux tests et à la démo sans clé API."""
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
    """Moteur sans API utilisé par les tests. Le runtime normal utilise ChromaRetriever."""

    def search(self, query: str, policies: list[Policy], limit: int = 5) -> list[SearchResult]:
        query_vector = _local_embedding(query)
        results = []
        for policy in policies:
            for chunk in chunk_policy(policy):
                score = _cosine(query_vector, _local_embedding(f"{policy.title} {chunk.text}"))
                results.append(SearchResult(policy, score, chunk.text, chunk.chunk_id))
        return sorted(results, key=lambda item: item.score, reverse=True)[:limit]


class ChromaRetriever:
    """Index ChromaDB persistant alimenté par un fournisseur d'embeddings multilingues."""

    def __init__(
        self,
        embedding_provider,
        persist_directory: str = ".local/chroma",
        collection_name: str = "hr_policy_chunks_v1",
        min_score: float = 0.35,
    ) -> None:
        import chromadb

        self.embedding_provider = embedding_provider
        self.min_score = min_score
        self._client = chromadb.PersistentClient(path=persist_directory)
        self._collection = self._client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )
        self._policies: dict[str, Policy] = {}

    def index_policies(self, policies: list[Policy]) -> int:
        chunks = []
        for policy in policies:
            self._policies[policy.policy_id] = policy
            self._collection.delete(where={"policy_id": policy.policy_id})
            chunks.extend(chunk_policy(policy))
        if not chunks:
            return 0
        texts = [chunk.text for chunk in chunks]
        embeddings = self.embedding_provider.embed(texts)
        self._collection.add(
            ids=[chunk.chunk_id for chunk in chunks],
            documents=texts,
            embeddings=embeddings,
            metadatas=[
                {"policy_id": chunk.policy_id, "position": chunk.position}
                for chunk in chunks
            ],
        )
        return len(chunks)

    def search(self, query: str, policies: list[Policy], limit: int = 5) -> list[SearchResult]:
        if not policies:
            return []
        for policy in policies:
            self._policies[policy.policy_id] = policy
        allowed_ids = [policy.policy_id for policy in policies]
        collection_size = self._collection.count()
        if collection_size == 0:
            return []
        query_embedding = self.embedding_provider.embed_query(query)
        raw = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=min(max(limit * 3, 10), collection_size),
            where={"policy_id": {"$in": allowed_ids}},
            include=["documents", "metadatas", "distances"],
        )
        per_policy: defaultdict[str, int] = defaultdict(int)
        results: list[SearchResult] = []
        for chunk_id, passage, metadata, distance in zip(
            raw["ids"][0], raw["documents"][0], raw["metadatas"][0], raw["distances"][0]
        ):
            policy_id = metadata["policy_id"]
            score = 1.0 - float(distance)
            if score < self.min_score or per_policy[policy_id] >= 2:
                continue
            policy = self._policies.get(policy_id)
            if not policy:
                continue
            results.append(SearchResult(policy, score, passage, chunk_id))
            per_policy[policy_id] += 1
            if len(results) >= limit:
                break
        return results
