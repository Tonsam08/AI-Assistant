from collections.abc import Sequence


class SentenceTransformerEmbeddingProvider:
    """Embeddings multilingues locaux : aucun texte n'est envoyé à un tiers."""

    def __init__(
        self,
        model=None,
        model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    ) -> None:
        if model is None:
            from sentence_transformers import SentenceTransformer

            model = SentenceTransformer(model_name)
        self.model = model
        self.model_name = model_name

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        if not texts:
            return []
        vectors = self.model.encode(
            list(texts),
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        return [list(map(float, vector)) for vector in vectors]

    def embed_query(self, text: str) -> list[float]:
        return self.embed([text])[0]


class OpenAIEmbeddingProvider:
    """Embeddings multilingues via l'API OpenAI, injectables dans ChromaDB."""

    def __init__(
        self,
        client=None,
        model: str = "text-embedding-3-large",
        dimensions: int = 1024,
    ) -> None:
        if client is None:
            from openai import OpenAI

            client = OpenAI()
        self.client = client
        self.model = model
        self.dimensions = dimensions

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        if not texts:
            return []
        response = self.client.embeddings.create(
            model=self.model,
            input=list(texts),
            dimensions=self.dimensions,
            encoding_format="float",
        )
        ordered = sorted(response.data, key=lambda item: item.index)
        return [list(item.embedding) for item in ordered]

    def embed_query(self, text: str) -> list[float]:
        return self.embed([text])[0]
