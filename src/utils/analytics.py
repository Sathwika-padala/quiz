"""Analytics for quiz performance."""

from typing import List, Dict, Any
from datetime import datetime


class QuizAnalytics:
    """Calculates performance statistics."""

    def __init__(self, results: List[Dict[str, Any]]):
        self.results = results

    def total_questions(self) -> int:
        return len(self.results)

    def correct_count(self) -> int:
        return sum(1 for r in self.results if r.get("is_correct", False))

    def incorrect_count(self) -> int:
        return self.total_questions() - self.correct_count()

    def percentage_score(self) -> float:
        if self.total_questions() == 0:
            return 0.0
        return (self.correct_count() / self.total_questions()) * 100

    def average_time_per_question(self) -> float:
        """Average seconds per question (if time_taken is in results)."""
        times = [r.get("time_taken", 0) for r in self.results if "time_taken" in r]
        if not times:
            return 0.0
        return sum(times) / len(times)

    def difficulty_breakdown(self) -> Dict[str, Dict[str, int]]:
        """Group results by difficulty."""
        breakdown = {}
        for r in self.results:
            difficulty = r.get("difficulty", "unknown")
            if difficulty not in breakdown:
                breakdown[difficulty] = {"correct": 0, "total": 0}
            breakdown[difficulty]["total"] += 1
            if r.get("is_correct"):
                breakdown[difficulty]["correct"] += 1
        return breakdown

    def summary(self) -> str:
        """Return formatted summary."""
        pct = self.percentage_score()
        return (
            f"Score: {self.correct_count()}/{self.total_questions()} ({pct:.1f}%)\n"
            f"Correct: {self.correct_count()}, Incorrect: {self.incorrect_count()}\n"
            f"Avg time/question: {self.average_time_per_question():.1f}s"
        )
