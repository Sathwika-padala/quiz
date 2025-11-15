"""Interactive quiz runner with scoring and timing."""

from typing import List, Optional, Dict, Any
from src.models.question_model import Question
from src.models.quiz_model import Quiz
from src.utils.timer import CountdownTimer
from src.utils.analytics import QuizAnalytics
import time


class QuizRunner:
    """Run a quiz interactively and track results."""

    def __init__(self, quiz: Quiz):
        self.quiz = quiz
        self.results = []
        self.start_time = None
        self.end_time = None

    def run(self) -> QuizAnalytics:
        """Run the quiz interactively."""
        print(f"\n{'='*60}")
        print(f"Quiz: {self.quiz.title}")
        print(f"Category: {self.quiz.category or 'General'}")
        print(f"Difficulty: {self.quiz.difficulty}")
        print(f"Questions: {len(self.quiz.questions)}")
        if self.quiz.timer_per_question:
            print(f"Time per question: {self.quiz.timer_per_question}s")
        print(f"{'='*60}\n")

        self.start_time = time.time()

        for idx, question in enumerate(self.quiz.questions, 1):
            result = self._run_question(idx, question)
            self.results.append(result)

        self.end_time = time.time()

        # Display summary
        analytics = QuizAnalytics(self.results)
        print(f"\n{'='*60}")
        print(analytics.summary())
        print(f"{'='*60}\n")

        return analytics

    def _run_question(self, question_num: int, question: Question) -> Dict[str, Any]:
        """Run a single question and collect answer."""
        print(f"{question_num}. {question.text}")
        for opt_idx, opt in enumerate(question.options):
            label = chr(ord("A") + opt_idx)
            print(f"   {label}. {opt}")

        timer = None
        if self.quiz.timer_per_question > 0:
            timer = CountdownTimer(self.quiz.timer_per_question)
            timer.start()
            print(f"   (Time limit: {self.quiz.timer_per_question}s)", end=" ")

        q_start = time.time()
        answer = self._get_answer(timer)
        q_time = time.time() - q_start

        if timer:
            timer.stop()

        # Validate and grade
        is_correct, chosen_text = self._validate_answer(answer, question)

        result = {
            "index": question_num,
            "question": question.text,
            "difficulty": question.difficulty,
            "chosen_letter": answer,
            "chosen_text": chosen_text,
            "correct_letter": question.answer,
            "is_correct": is_correct,
            "time_taken": q_time,
        }

        if is_correct:
            print("✓ Correct!\n")
        else:
            correct_text = ""
            try:
                idx = ord(question.answer.upper()) - ord("A")
                correct_text = question.options[idx]
            except Exception:
                correct_text = question.answer
            print(f"✗ Incorrect. Answer: {question.answer} ({correct_text})\n")

        return result

    def _get_answer(self, timer: Optional[CountdownTimer]) -> str:
        """Get user's answer with validation."""
        while True:
            if timer and timer.is_expired():
                print("TIME UP!")
                return ""

            ans = input("Your answer (letter) or 'skip'/'quit': ").strip().upper()

            if ans in {"SKIP", "S"}:
                print("Skipped\n")
                return ""
            if ans in {"QUIT", "Q"}:
                print("Quiz terminated.")
                raise KeyboardInterrupt()
            if len(ans) == 1 and ans.isalpha():
                return ans

            print("Invalid. Enter A, B, C, D, or 'skip'/'quit'.")

    def _validate_answer(self, answer: str, question: Question) -> tuple:
        """Check if answer is correct."""
        if not answer:
            return False, ""

        try:
            idx = ord(answer) - ord("A")
            chosen_text = question.options[idx]
        except (ValueError, IndexError):
            return False, ""

        is_correct = answer == question.answer
        return is_correct, chosen_text
