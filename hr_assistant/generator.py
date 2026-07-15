from .models import SearchResult
from .security import contains_prompt_injection


class ControlledDraftGenerator:
    """Générateur local sans LLM externe, avec citations et garde-fous."""

    def draft_answer(self, sources: tuple[SearchResult, ...]) -> str:
        safe_sources = [item for item in sources if not contains_prompt_injection(item.policy.content)]
        if not safe_sources:
            raise ValueError("No safe source available")
        excerpts = "\n\n".join(
            f"• [{item.policy.policy_id}] {item.policy.title}: {item.policy.content}"
            for item in safe_sources[:2]
        )
        return (
            "Réponse préparée à partir des politiques autorisées :\n\n"
            f"{excerpts}\n\n"
            "Cette réponse doit être validée par les RH avant tout envoi."
        )

    def draft_information_request(self) -> str:
        return "Merci de préciser le sujet, le pays concerné et les éléments nécessaires au traitement de votre demande."
