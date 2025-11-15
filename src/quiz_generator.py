import random
from pathlib import Path
import json
from typing import List
from .question_model import Question


def generate_quiz(questions: List[Question], count: int = 5, topic: str | None = None) -> List[Question]:
    """Return a random sample of questions.

    If `topic` is provided, only questions whose `topic` matches (case-insensitive)
    will be considered.
    """
    pool = questions
    if topic:
        pool = [q for q in questions if q.topic and q.topic.lower() == topic.lower()]
        if not pool:
            raise ValueError(f"No questions found for topic: {topic}")
    count = min(count, len(pool))

    def _make_shuffled_question(q: Question) -> Question:
        # Create a shuffled copy of the question and set answer as a letter (A/B/...)
        opts = list(q.options)
        # Determine original correct option text (supports both text and letter answers)
        correct_text = None
        if isinstance(q.answer, str) and len(q.answer) == 1 and q.answer.isalpha():
            # letter given relative to original ordering
            idx = ord(q.answer.upper()) - ord("A")
            if 0 <= idx < len(q.options):
                correct_text = q.options[idx]
        if correct_text is None:
            # fallback: match by option text
            for o in q.options:
                if o == q.answer:
                    correct_text = o
                    break
        if correct_text is None and q.options:
            # last resort: assume first option
            correct_text = q.options[0]

        random.shuffle(opts)
        try:
            new_idx = opts.index(correct_text)
        except ValueError:
            new_idx = 0
        new_answer_letter = chr(ord("A") + new_idx)
        return Question(id=q.id, text=q.text, options=opts, answer=new_answer_letter, topic=q.topic)

    sampled = random.sample(pool, count)
    return [_make_shuffled_question(q) for q in sampled]


def save_quiz_text(questions: List[Question], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        # Optional header with topics covered
        topics = sorted({q.topic for q in questions if q.topic})
        if topics:
            f.write("Topics: " + ", ".join(topics) + "\n\n")
        for idx, q in enumerate(questions, start=1):
            f.write(f"{idx}. {q.text}\n")
            for opt_idx, opt in enumerate(q.options):
                label = chr(ord("A") + opt_idx)
                f.write(f"   {label}. {opt}\n")
            f.write("\n")
        f.write("Answer Key:\n")
        for idx, q in enumerate(questions, start=1):
            # q.answer is now a letter; show both letter and text when possible
            ans = q.answer
            ans_text = ""
            if isinstance(ans, str) and len(ans) == 1 and ans.isalpha():
                try:
                    ans_text = q.options[ord(ans.upper()) - ord("A")]
                except Exception:
                    ans_text = ""
            else:
                ans_text = str(ans)
            if ans_text:
                f.write(f"{idx}: {ans} ({ans_text})\n")
            else:
                f.write(f"{idx}: {ans}\n")


def save_quiz_json(questions: List[Question], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump([q.to_dict() for q in questions], f, indent=2, ensure_ascii=False)
