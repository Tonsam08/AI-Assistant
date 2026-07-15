from .classifier import classify_request
from .models import Decision, UserContext, WorkflowResult
from .policies import accessible_policies


MIN_CLASSIFICATION_CONFIDENCE = 0.60
MIN_RETRIEVAL_SCORE = 0.12


def process_request(text: str, user: UserContext, policies, retriever) -> WorkflowResult:
    text = text.strip()
    classification = classify_request(text)

    if not text:
        return WorkflowResult(
            Decision.REQUEST_INFO,
            classification,
            "Merci de préciser votre demande afin que les RH puissent la traiter.",
        )
    if classification.sensitive:
        return WorkflowResult(
            Decision.ESCALATE,
            classification,
            "Cette demande est sensible et doit être examinée par une personne des RH.",
        )
    if classification.missing_information or classification.confidence < MIN_CLASSIFICATION_CONFIDENCE:
        return WorkflowResult(
            Decision.REQUEST_INFO,
            classification,
            "Le sujet de la demande n’est pas assez précis. Merci d’ajouter le contexte nécessaire.",
        )

    allowed = accessible_policies(policies, user)
    results = retriever.search(text, allowed)
    relevant = tuple(result for result in results if result.score >= MIN_RETRIEVAL_SCORE)
    if not relevant:
        return WorkflowResult(
            Decision.ESCALATE,
            classification,
            "Aucune politique accessible ne permet de préparer une réponse fiable.",
        )

    excerpts = "\n\n".join(
        f"• {result.policy.title} : {result.policy.content}" for result in relevant[:2]
    )
    message = (
        "Réponse préparée à partir des politiques accessibles :\n\n"
        f"{excerpts}\n\n"
        "Cette réponse doit être validée par les RH avant envoi."
    )
    return WorkflowResult(Decision.ANSWER, classification, message, relevant)
