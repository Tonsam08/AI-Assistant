from dataclasses import dataclass, field
from enum import Enum


class Decision(str, Enum):
    ANSWER = "answer"
    ESCALATE = "escalate"
    REQUEST_INFO = "request_info"


class Action(str, Enum):
    SEARCH_POLICY = "search_policy"
    DRAFT_ANSWER = "draft_answer"
    REQUEST_INFORMATION = "request_information"
    ESCALATE_HUMAN = "escalate_human"


@dataclass(frozen=True)
class UserContext:
    user_id: str
    country: str
    groups: frozenset[str] = field(default_factory=frozenset)


@dataclass(frozen=True)
class Classification:
    topic: str
    sensitive: bool
    confidence: float
    missing_information: tuple[str, ...] = ()


@dataclass(frozen=True)
class Policy:
    policy_id: str
    title: str
    country: str
    allowed_groups: frozenset[str]
    content: str
    language: str = "en"
    owner: str = "unassigned"
    valid_until: str | None = None
    sensitive: bool = False


@dataclass(frozen=True)
class SearchResult:
    policy: Policy
    score: float


@dataclass(frozen=True)
class WorkflowResult:
    decision: Decision
    classification: Classification
    message: str
    sources: tuple[SearchResult, ...] = ()
    route: "RouteDecision | None" = None
    trace_id: str | None = None


@dataclass(frozen=True)
class RouteDecision:
    topic: str
    sensitive: bool
    confidence: float
    action: Action
    requires_human_review: bool
    reason: str
    allowed_tools: tuple[str, ...] = ()

    def as_dict(self) -> dict:
        return {
            "topic": self.topic,
            "sensitive": self.sensitive,
            "confidence": self.confidence,
            "action": self.action.value,
            "requires_human_review": self.requires_human_review,
            "reason": self.reason,
            "allowed_tools": list(self.allowed_tools),
        }
