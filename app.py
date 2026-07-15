import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from hr_assistant.models import Decision, UserContext
from hr_assistant.audit import AuditStore
from hr_assistant.embeddings import SentenceTransformerEmbeddingProvider
from hr_assistant.generator import ControlledDraftGenerator, OpenAIDraftGenerator
from hr_assistant.policies import load_policies
from hr_assistant.retriever import ChromaRetriever, LocalRetriever
from hr_assistant.workflow import process_request


load_dotenv()
st.set_page_config(page_title="Assistant RH — Prototype", page_icon="🧭", layout="centered")


@st.cache_resource
def get_retriever():
    try:
        provider = SentenceTransformerEmbeddingProvider(
            model_name=os.getenv(
                "MULTILINGUAL_EMBEDDING_MODEL",
                "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
            )
        )
        retriever = ChromaRetriever(
            provider,
            persist_directory=os.getenv("CHROMA_PERSIST_DIRECTORY", ".local/chroma"),
            min_score=float(os.getenv("RAG_MIN_SCORE", "0.35")),
        )
        return retriever, "ChromaDB + embeddings multilingues locaux", None
    except Exception as exc:
        return LocalRetriever(), "moteur lexical de secours", str(exc)


@st.cache_resource
def get_generator():
    if os.getenv("OPENAI_API_KEY"):
        return OpenAIDraftGenerator(model=os.getenv("OPENAI_CHAT_MODEL", "gpt-5.6-terra")), "OpenAI Responses API"
    return ControlledDraftGenerator(), "générateur local de secours"


policies = load_policies(Path(__file__).parent / "data" / "policies.json")
retriever, retriever_name, retriever_error = get_retriever()
if isinstance(retriever, ChromaRetriever):
    retriever.index_policies(policies)
generator, generator_name = get_generator()
audit_store = AuditStore()

st.title("Assistant RH")
st.caption("Prototype avec données fictives — aucune réponse n’est envoyée automatiquement")

with st.sidebar:
    st.subheader("Utilisateur de démonstration")
    country = st.selectbox("Pays", ["FR", "DE", "IN"], index=0)
    role = st.selectbox("Groupe d’accès", ["employees", "hr"], index=0)
    st.caption(f"Recherche : {retriever_name}")
    st.caption(f"Génération : {generator_name}")
    if retriever_error:
        st.warning("Le modèle multilingue local n'est pas disponible. Recherche de secours activée.")

request = st.text_area(
    "Demande RH",
    placeholder="Exemple : Comment déposer une demande de congés ?",
    height=140,
)

if st.button("Préparer la réponse", type="primary", use_container_width=True):
    user = UserContext("demo-user", country, frozenset({role}))
    result = process_request(
        request, user, policies, retriever,
        generator=generator, audit_store=audit_store,
    )

    st.subheader("Décision")
    labels = {
        Decision.ANSWER: "Réponse à valider",
        Decision.ESCALATE: "Transmission aux RH",
        Decision.REQUEST_INFO: "Informations complémentaires nécessaires",
    }
    st.info(labels[result.decision])
    st.write(result.message)

    if result.sources:
        st.subheader("Passages retenus pour répondre")
        for index, item in enumerate(result.sources, start=1):
            st.markdown(
                f"**[S{index}] {item.policy.title}** — pertinence {item.score:.2f}  \n"
                f"`{item.chunk_id}`"
            )
            st.info(item.passage or item.policy.content)

    with st.expander("Détails de traitement"):
        st.json({
            "topic": result.classification.topic,
            "sensitive": result.classification.sensitive,
            "classification_confidence": result.classification.confidence,
            "route": result.route.as_dict() if result.route else None,
            "trace_id": result.trace_id,
            "sources": [
                {
                    "title": item.policy.title,
                    "policy_id": item.policy.policy_id,
                    "chunk_id": item.chunk_id,
                    "score": round(item.score, 3),
                }
                for item in result.sources
            ],
        })
