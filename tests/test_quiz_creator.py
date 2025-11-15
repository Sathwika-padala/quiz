"""Test for quiz creator."""

import pytest
from pathlib import Path
from src.creators.quiz_creator import QuizCreator


def test_load_questions():
    creator = QuizCreator()
    assert len(creator.questions) > 0


def test_get_available_categories():
    creator = QuizCreator()
    categories = creator.get_available_categories()
    assert len(categories) > 0
    assert "Geography" in categories


def test_create_quiz_by_topic():
    creator = QuizCreator()
    quiz = creator.create_quiz_by_topic("Test Quiz", "Math", count=1)
    assert quiz.title == "Test Quiz"
    assert len(quiz.questions) == 1
    assert all(q.topic == "Math" for q in quiz.questions)


def test_create_quiz_by_topic_not_found():
    creator = QuizCreator()
    with pytest.raises(ValueError):
        creator.create_quiz_by_topic("Test", "NonexistentTopic", count=1)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
