"""Global configuration settings."""

import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
QUIZZES_DIR = DATA_DIR / "quizzes"
EXPORTS_DIR = BASE_DIR / "exports"
PDF_DIR = EXPORTS_DIR / "quiz_pdfs"
REPORTS_DIR = EXPORTS_DIR / "quiz_reports"

# Ensure directories exist
for d in [DATA_DIR, QUIZZES_DIR, EXPORTS_DIR, PDF_DIR, REPORTS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# File paths
QUESTIONS_FILE = DATA_DIR / "questions.json"
CATEGORIES_FILE = DATA_DIR / "categories.json"
DIFFICULTY_LEVELS_FILE = DATA_DIR / "difficulty_levels.json"
LEADERBOARD_FILE = DATA_DIR / "leaderboard.json"

# Default settings
DEFAULT_TIMER_PER_QUESTION = 60  # seconds
DEFAULT_DIFFICULTY = "medium"
DEFAULT_CATEGORY = "General"

# Difficulty levels
DIFFICULTY_LEVELS = ["easy", "medium", "hard"]

# Quiz settings
MIN_QUESTIONS = 1
MAX_QUESTIONS = 100
