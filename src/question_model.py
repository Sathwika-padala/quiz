from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any


@dataclass
class Question:
    id: str
    text: str
    options: List[str]
    answer: str
    topic: Optional[str] = ""

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
        )
