"""Adaptive difficulty engine."""

from typing import List, Dict, Any


class AdaptiveEngine:
    """Adjust quiz difficulty based on user performance."""

    def __init__(self, success_threshold: float = 0.7):
        """
        Initialize adaptive engine.

        Args:
            success_threshold: Performance above this % triggers difficulty increase.
        """
        self.success_threshold = success_threshold
        self.session_results = []

    def log_result(self, result: Dict[str, Any]) -> None:
        """Log a question result."""
        self.session_results.append(result)

    def should_increase_difficulty(self) -> bool:
        """Check if performance warrants increased difficulty."""
        if len(self.session_results) < 3:
            return False
        recent = self.session_results[-3:]
        correct = sum(1 for r in recent if r.get("is_correct"))
        return correct / len(recent) >= self.success_threshold

    def should_decrease_difficulty(self) -> bool:
        """Check if performance warrants decreased difficulty."""
        if len(self.session_results) < 3:
            return False
        recent = self.session_results[-3:]
        correct = sum(1 for r in recent if r.get("is_correct"))
        return correct / len(recent) < 0.3

    def get_performance_summary(self) -> Dict[str, Any]:
        """Return performance summary."""
        total = len(self.session_results)
        if total == 0:
            return {"total": 0, "correct": 0, "percentage": 0}
        
        correct = sum(1 for r in self.session_results if r.get("is_correct"))
        by_difficulty = {}
        for r in self.session_results:
            diff = r.get("difficulty", "unknown")
            if diff not in by_difficulty:
                by_difficulty[diff] = {"total": 0, "correct": 0}
            by_difficulty[diff]["total"] += 1
            if r.get("is_correct"):
                by_difficulty[diff]["correct"] += 1

        return {
            "total": total,
            "correct": correct,
            "percentage": (correct / total * 100) if total > 0 else 0,
            "by_difficulty": by_difficulty,
        }
