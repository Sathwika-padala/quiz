# Quiz Generator

A comprehensive Python quiz application with topic/difficulty filtering, interactive runner, leaderboard, and adaptive difficulty.

## Project Structure

```
quiz/
├── data/
│   ├── questions.json          # Quiz questions with topics & difficulty
│   ├── categories.json         # Available categories
│   ├── difficulty_levels.json  # Difficulty settings
│   ├── leaderboard.json        # User scores
│   └── quizzes/               # Saved quiz files
├── exports/
│   ├── quiz_pdfs/             # Exported PDF quizzes
│   └── quiz_reports/          # Score reports
├── src/
│   ├── models/                # Data models (Question, Quiz)
│   ├── creators/              # Quiz creation logic
│   ├── runners/               # Quiz execution & adaptive engine
│   ├── utils/                 # Utilities (timer, shuffle, analytics, leaderboard, etc.)
│   ├── ui/                    # Terminal UI (menus, CLI interface)
│   ├── main.py               # Entry point
│   └── config.py             # Configuration
├── tests/                      # Unit tests
└── README.md
```

## Features

- **Topic-based Quiz Generation:** Create quizzes filtered by topic (Geography, Chemistry, etc.)
- **Difficulty Levels:** Generate quizzes by difficulty (easy, medium, hard)
- **Interactive Runner:** Answer questions with letter input; supports skip/quit
- **Leaderboard:** Track user scores and view rankings
- **Adaptive Difficulty:** Adjust quiz difficulty based on user performance
- **Shuffled Options:** Question options are randomized each time
- **PDF Export:** Export quizzes and results as PDF (placeholder)
- **User History:** View past quiz performance

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

Run the main application (interactive menu):

```bash
python -m src.main
```

This opens a menu where you can:
1. Generate quizzes by topic
2. Generate quizzes by difficulty
3. View leaderboard
4. View your quiz history

## Running Tests

```bash
pytest tests/ -v
```

## Configuration

Edit `src/config.py` to customize settings like timer duration and file paths.

## Sample Questions

The `data/questions.json` includes sample questions across multiple topics and difficulty levels.

## Notes

- PDF export is a placeholder; integrate `reportlab` for real PDF generation
- Leaderboard stored in JSON; migrate to database for production
- Current version uses CLI interface; GUI is optional

## Future Enhancements

- Web UI with Flask/FastAPI
- Database integration
- Spaced repetition mode
- Real PDF export
- User authentication
