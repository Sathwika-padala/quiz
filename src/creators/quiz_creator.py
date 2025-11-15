"""Quiz creator module for building quizzes interactively."""

from typing import Optional, List
from pathlib import Path
from src.models.question_model import Question
from src.models.quiz_model import Quiz
from src.utils.file_handler import load_json, save_json
from src.config import QUESTIONS_FILE, QUIZZES_DIR, CATEGORIES_FILE
import uuid


class QuizCreator:
    """Create quizzes from existing questions."""

    def __init__(self, questions_file: Path = QUESTIONS_FILE):
        self.questions_file = questions_file
        self.questions = self._load_questions()

    def _load_questions(self) -> List[Question]:
        """Load questions from file."""
        data = load_json(self.questions_file)
        if not isinstance(data, list):
            return []
        return [Question.from_dict(q) for q in data]

    def create_quiz_by_topic(
        self, title: str, topic: str, count: int = 5, shuffle: bool = True
    ) -> Quiz:
        """Create a quiz for a specific topic."""
        import random

        pool = [q for q in self.questions if q.topic and q.topic.lower() == topic.lower()]
        if not pool:
            raise ValueError(f"No questions found for topic: {topic}")

        count = min(count, len(pool))
        selected = random.sample(pool, count)

        if shuffle:
            for q in selected:
                from src.utils.shuffle import shuffle_options

                q.options, q.answer = shuffle_options(q.options, q.answer)

        quiz = Quiz(
            id=str(uuid.uuid4()),
            title=title,
            questions=selected,
            category=topic,
        )
        return quiz

    def create_quiz_by_difficulty(
        self, title: str, difficulty: str, count: int = 5, shuffle: bool = True
    ) -> Quiz:
        """Create a quiz with specific difficulty."""
        import random

        pool = [q for q in self.questions if q.difficulty == difficulty.lower()]
        if not pool:
            raise ValueError(f"No questions found with difficulty: {difficulty}")

        count = min(count, len(pool))
        selected = random.sample(pool, count)

        if shuffle:
            for q in selected:
                from src.utils.shuffle import shuffle_options

                q.options, q.answer = shuffle_options(q.options, q.answer)

        quiz = Quiz(
            id=str(uuid.uuid4()),
            title=title,
            questions=selected,
            difficulty=difficulty,
        )
        return quiz

    def save_quiz(self, quiz: Quiz, filename: str = None) -> str:
        """Save quiz to file."""
        if filename is None:
            filename = f"{quiz.title.replace(' ', '_')}.json"
        path = QUIZZES_DIR / filename
        save_json(path, quiz.to_dict())
        return str(path)

    def get_available_categories(self) -> List[str]:
        """Get list of unique topics/categories."""
        categories = sorted({q.topic for q in self.questions if q.topic})
        return categories

    def get_available_difficulties(self) -> List[str]:
        """Get list of unique difficulties."""
        difficulties = sorted({q.difficulty for q in self.questions if q.difficulty})
        return difficulties
