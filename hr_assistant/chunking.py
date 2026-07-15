import hashlib
import re
from dataclasses import dataclass

from .models import Policy


@dataclass(frozen=True)
class PolicyChunk:
    chunk_id: str
    policy_id: str
    text: str
    position: int


def _sentences(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+|\n+", text) if part.strip()]


def chunk_policy(policy: Policy, target_words: int = 160, overlap_sentences: int = 1) -> list[PolicyChunk]:
    """Découpe par phrases, avec chevauchement et identifiants stables."""
    sentences = _sentences(policy.content)
    if not sentences:
        return []
    chunks: list[PolicyChunk] = []
    start = 0
    while start < len(sentences):
        current: list[str] = []
        words = 0
        end = start
        while end < len(sentences) and (words < target_words or not current):
            current.append(sentences[end])
            words += len(sentences[end].split())
            end += 1
        text = " ".join(current)
        digest = hashlib.sha256(f"{policy.policy_id}:{start}:{text}".encode("utf-8")).hexdigest()[:16]
        chunks.append(PolicyChunk(f"{policy.policy_id}:{digest}", policy.policy_id, text, len(chunks)))
        if end >= len(sentences):
            break
        start = max(start + 1, end - overlap_sentences)
    return chunks
