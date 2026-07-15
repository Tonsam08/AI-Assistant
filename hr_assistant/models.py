from dataclasses import dataclass, field
from enum import Enum


class Decision(str, Enum):
    ANSWER = "answer"
    ESCALATE = "escalate"
    REQUEST_INFO = "request_info"


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
