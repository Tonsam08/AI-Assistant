from .audit import AuditStore
from .classifier import classify_request
from .generator import ControlledDraftGenerator
from .models import Action, Decision, UserContext, WorkflowResult
from .policies import accessible_policies
from .router import initial_route, route_after_search


MIN_RETRIEVAL_SCORE = 0.12


def process_request(
    text: str, user: UserContext, policies, retriever,
    generator=None, audit_store: AuditStore | None = None,
) -> WorkflowResult:
    text = text.strip()
    generator = generator or ControlledDraftGenerator()
    classification = classify_request(text)
    route = initial_route(classification)

    if route.action is Action.ESCALATE_HUMAN:
        message = "Cette demande doit être examinée par une personne des RH."
        decision = Decision.ESCALATE
        sources = ()
    elif route.action is Action.REQUEST_INFORMATION:
        message = generator.draft_information_request()
        decision = Decision.REQUEST_INFO
        sources = ()
    else:
        allowed = accessible_policies(policies, user)
        results = retriever.search(text, allowed)
        sources = tuple(result for result in results if result.score >= MIN_RETRIEVAL_SCORE)
        sources = generator.approved_sources(sources)
        route = route_after_search(classification, bool(sources))
        if route.action is Action.ESCALATE_HUMAN:
            message = "Aucune politique accessible ne permet de préparer une réponse fiable."
            decision = Decision.ESCALATE
        else:
            try:
                message = generator.draft_answer(sources, question=text)
                decision = Decision.ANSWER
            except ValueError:
                route = route_after_search(classification, False)
                message = "Les sources trouvées ne peuvent pas être utilisées en sécurité."
                decision = Decision.ESCALATE
                sources = ()

    trace_id = audit_store.record(text, route) if audit_store else None
    return WorkflowResult(decision, classification, message, sources, route, trace_id)
