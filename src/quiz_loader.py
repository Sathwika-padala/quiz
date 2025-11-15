from pathlib import Path
import json
from typing import List
from .question_model import Question


def load_questions(path: Path) -> List[Question]:
    p = Path(path)
    with p.open(encoding="utf-8") as f:
        data = json.load(f)
    questions = []
    for i, item in enumerate(data):
        if "id" not in item:
            item["id"] = str(i + 1)
        questions.append(Question.from_dict(item))
    return questions
