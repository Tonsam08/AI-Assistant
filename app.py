from pathlib import Path

import streamlit as st

from hr_assistant.models import Decision, UserContext
from hr_assistant.policies import load_policies
from hr_assistant.retriever import ChromaRetriever, LocalRetriever
from hr_assistant.workflow import process_request


st.set_page_config(page_title="Assistant RH — Prototype", page_icon="🧭", layout="centered")


@st.cache_resource
def get_retriever():
    try:
        return ChromaRetriever(), "ChromaDB"
    except Exception:
        return LocalRetriever(), "moteur local de secours"


policies = load_policies(Path(__file__).parent / "data" / "policies.json")
retriever, retriever_name = get_retriever()

st.title("Assistant RH")
st.caption("Prototype avec données fictives — aucune réponse n’est envoyée automatiquement")

with st.sidebar:
    st.subheader("Utilisateur de démonstration")
    country = st.selectbox("Pays", ["FR", "DE", "IN"], index=0)
    role = st.selectbox("Groupe d’accès", ["employees", "hr"], index=0)
    st.caption(f"Recherche : {retriever_name}")

request = st.text_area(
    "Demande RH",
    placeholder="Exemple : Comment déposer une demande de congés ?",
    height=140,
)

if st.button("Préparer la réponse", type="primary", use_container_width=True):
    user = UserContext("demo-user", country, frozenset({role}))
    result = process_request(request, user, policies, retriever)

    st.subheader("Décision")
    labels = {
        Decision.ANSWER: "Réponse à valider",
        Decision.ESCALATE: "Transmission aux RH",
        Decision.REQUEST_INFO: "Informations complémentaires nécessaires",
    }
    st.info(labels[result.decision])
    st.write(result.message)

    with st.expander("Détails de traitement"):
        st.json({
            "topic": result.classification.topic,
            "sensitive": result.classification.sensitive,
            "classification_confidence": result.classification.confidence,
            "sources": [
                {"title": item.policy.title, "score": round(item.score, 3)}
                for item in result.sources
            ],
        })
