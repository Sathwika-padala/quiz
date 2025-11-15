"""Leaderboard management."""

from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
from .file_handler import load_json, append_to_json_list, save_json


class LeaderboardHandler:
    """Manage user scores and leaderboard."""

    def __init__(self, leaderboard_file: Path):
        self.leaderboard_file = leaderboard_file

    def add_score(self, username: str, quiz_title: str, score: float, total: int) -> None:
        """Add a score entry to leaderboard."""
        from datetime import datetime, timezone
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "username": username,
            "quiz_title": quiz_title,
            "score": score,
            "total": total,
            "percentage": (score / total * 100) if total > 0 else 0,
        }
        append_to_json_list(self.leaderboard_file, entry)

    def get_leaderboard(self, limit: int = 10) -> List[Dict]:
        """Get top scores."""
        data = load_json(self.leaderboard_file)
        if not isinstance(data, list):
            return []
        # Sort by percentage descending
        sorted_data = sorted(data, key=lambda x: x.get("percentage", 0), reverse=True)
        return sorted_data[:limit]

    def get_user_history(self, username: str) -> List[Dict]:
        """Get all scores for a user."""
        data = load_json(self.leaderboard_file)
        if not isinstance(data, list):
            return []
        return [d for d in data if d.get("username") == username]

    def display_leaderboard(self, limit: int = 10) -> str:
        """Format leaderboard for display."""
        scores = self.get_leaderboard(limit)
        if not scores:
            return "Leaderboard is empty."
        
        output = "=== TOP SCORES ===\n"
        output += f"{'Rank':<5} {'User':<15} {'Quiz':<20} {'Score':<10} {'%':<6}\n"
        output += "-" * 60 + "\n"
        
        for idx, entry in enumerate(scores, 1):
            user = entry.get("username", "Unknown")[:15]
            quiz = entry.get("quiz_title", "Unknown")[:20]
            score = entry.get("score", 0)
            pct = entry.get("percentage", 0)
            output += f"{idx:<5} {user:<15} {quiz:<20} {score:<10} {pct:.1f}%\n"
        
        return output
