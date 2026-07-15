from types import SimpleNamespace

import pytest

from hr_assistant.embeddings import OpenAIEmbeddingProvider, SentenceTransformerEmbeddingProvider
from hr_assistant.generator import ExternalGenerationNotAllowed, OpenAIDraftGenerator
from hr_assistant.models import Policy, SearchResult


class FakeSentenceModel:
    def encode(self, texts, **kwargs):
        assert kwargs["normalize_embeddings"] is True
        return [[len(text), 1] for text in texts]


def source(*, allowed=True, sensitive=False):
    policy = Policy(
        "fr-leave", "Congés", "FR", frozenset({"employees"}),
        "La demande doit être déposée dans le portail RH.", "fr", "demo",
        sensitive=sensitive, external_ai_allowed=allowed,
    )
    return SearchResult(policy, 0.91, policy.content, "fr-leave:0")


def test_local_multilingual_provider_normalizes_and_returns_floats():
    provider = SentenceTransformerEmbeddingProvider(model=FakeSentenceModel())
    assert provider.embed(["congés", "urlaub"]) == [[6.0, 1.0], [6.0, 1.0]]


def test_openai_embedding_provider_preserves_api_order():
    embeddings = SimpleNamespace(create=lambda **kwargs: SimpleNamespace(data=[
        SimpleNamespace(index=1, embedding=[0.0, 1.0]),
        SimpleNamespace(index=0, embedding=[1.0, 0.0]),
    ]))
    provider = OpenAIEmbeddingProvider(client=SimpleNamespace(embeddings=embeddings))
    assert provider.embed(["fr", "de"]) == [[1.0, 0.0], [0.0, 1.0]]


def test_openai_generator_redacts_request_and_requires_valid_citations():
    captured = {}

    def create(**kwargs):
        captured.update(kwargs)
        return SimpleNamespace(output_text="Déposez la demande dans le portail [S1].\n\nBrouillon à valider par les RH.")

    client = SimpleNamespace(responses=SimpleNamespace(create=create))
    generator = OpenAIDraftGenerator(client=client, model="test-model")
    answer = generator.draft_answer((source(),), "Écris à sami@example.com pour mes congés")
    assert "sami@example.com" not in captured["input"]
    assert "[EMAIL]" in captured["input"]
    assert "[S1]" in answer
    assert captured["store"] is False


def test_openai_generator_rejects_unapproved_policy():
    generator = OpenAIDraftGenerator(client=SimpleNamespace(responses=None), model="test")
    with pytest.raises(ExternalGenerationNotAllowed):
        generator.draft_answer((source(allowed=False),), "Question")
