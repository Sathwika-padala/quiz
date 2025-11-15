from dataclasses import dataclass, asdict, field
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from .question_model import Question


@dataclass
class Quiz:
    """Represents a quiz."""

    id: str
    title: str
    questions: List[Question] = field(default_factory=list)
    category: str = ""
    difficulty: str = "mixed"  # easy, medium, hard, mixed
    timer_per_question: int = 0  # seconds; 0 = no timer
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "questions": [q.to_dict() for q in self.questions],
            "category": self.category,
            "difficulty": self.difficulty,
            "timer_per_question": self.timer_per_question,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Quiz":
        return Quiz(
            id=d.get("id", ""),
            title=d.get("title", ""),
            questions=[Question.from_dict(q) for q in d.get("questions", [])],
            category=d.get("category", ""),
            difficulty=d.get("difficulty", "mixed"),
            timer_per_question=d.get("timer_per_question", 0),
            created_at=d.get("created_at", datetime.now(timezone.utc).isoformat()),
        )
