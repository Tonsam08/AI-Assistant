from .models import Action, Classification, RouteDecision


MIN_CLASSIFICATION_CONFIDENCE = 0.60


def initial_route(classification: Classification) -> RouteDecision:
    if classification.sensitive:
        return RouteDecision(
            classification.topic, True, classification.confidence,
            Action.ESCALATE_HUMAN, True, "Sensitive request detected", (),
        )
    if classification.missing_information or classification.confidence < MIN_CLASSIFICATION_CONFIDENCE:
        return RouteDecision(
            classification.topic, False, classification.confidence,
            Action.REQUEST_INFORMATION, True, "Topic or intent is insufficiently clear",
            ("draft_information_request",),
        )
    return RouteDecision(
        classification.topic, False, classification.confidence,
        Action.SEARCH_POLICY, True, "Request can be searched in accessible policies",
        ("policy_search",),
    )


def route_after_search(classification: Classification, has_relevant_policy: bool) -> RouteDecision:
    if not has_relevant_policy:
        return RouteDecision(
            classification.topic, classification.sensitive, classification.confidence,
            Action.ESCALATE_HUMAN, True, "No sufficiently relevant accessible policy", (),
        )
    return RouteDecision(
        classification.topic, False, classification.confidence,
        Action.DRAFT_ANSWER, True, "Relevant accessible policy found",
        ("draft_answer",),
    )
