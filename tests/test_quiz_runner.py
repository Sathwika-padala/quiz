"""Test for quiz runner."""

import pytest
from src.creators.quiz_creator import QuizCreator
from src.runners.quiz_runner import QuizRunner


def test_quiz_runner_init():
    creator = QuizCreator()
    quiz = creator.create_quiz_by_topic("Test", "Math", count=2)
    runner = QuizRunner(quiz)
    assert runner.quiz.title == "Test"
    assert len(runner.results) == 0


def test_validate_answer():
    creator = QuizCreator()
    quiz = creator.create_quiz_by_topic("Test", "Math", count=1)
    runner = QuizRunner(quiz)
    question = quiz.questions[0]
    
    # Test correct answer
    is_correct, text = runner._validate_answer(question.answer, question)
    assert is_correct is True
    
    # Test incorrect answer
    wrong_letter = chr(ord(question.answer) + 1) if ord(question.answer) < ord("D") else "A"
    is_correct, text = runner._validate_answer(wrong_letter, question)
    assert is_correct is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
