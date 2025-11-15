from dataclasses import dataclass, asdict, field
from typing import Optional, Dict, Any


@dataclass
class Question:
    """Represents a single quiz question."""

    id: str
    text: str
    options: list
    answer: str  # Letter (A/B/C/D) or text
    topic: Optional[str] = ""
    difficulty: Optional[str] = "medium"  # easy, medium, hard
    explanation: Optional[str] = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Question":
        return Question(
            id=str(d.get("id", "")),
            text=d["text"],
            options=d.get("options", []),
            answer=d["answer"],
            topic=d.get("topic", ""),
            difficulty=d.get("difficulty", "medium"),
            explanation=d.get("explanation", ""),
        )
