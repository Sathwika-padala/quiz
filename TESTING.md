# Testing Guide for Quiz Generator

## Automated Tests

Run all unit tests:
```bash
pytest tests/ -v
```

Run specific test file:
```bash
pytest tests/test_quiz_creator.py -v
```

Run with coverage:
```bash
pip install pytest-cov
pytest tests/ --cov=src --cov-report=html
```

## Manual Testing

### 1. Test Quiz Creator (Programmatic)
```bash
python << 'PYEOF'
from src.creators.quiz_creator import QuizCreator

creator = QuizCreator()

# List available topics
print("Topics:", creator.get_available_categories())
print("Difficulties:", creator.get_available_difficulties())

# Create quiz by topic
quiz = creator.create_quiz_by_topic("Geography Test", "Geography", count=2)
print(f"\nCreated {len(quiz.questions)} questions")
for q in quiz.questions:
    print(f"  - {q.text}")

# Save quiz
path = creator.save_quiz(quiz)
print(f"Saved to: {path}")
PYEOF
```

### 2. Test Quiz Runner (Interactive)
```bash
python << 'PYEOF'
from src.creators.quiz_creator import QuizCreator
from src.runners.quiz_runner import QuizRunner

creator = QuizCreator()
quiz = creator.create_quiz_by_topic("Quick Test", "Math", count=1)
runner = QuizRunner(quiz)
analytics = runner.run()
PYEOF
```

Then provide answers when prompted (enter A, B, C, or D).

### 3. Test Leaderboard
```bash
python << 'PYEOF'
from src.utils.leaderboard_handler import LeaderboardHandler
from src.config import LEADERBOARD_FILE

lb = LeaderboardHandler(LEADERBOARD_FILE)

# Add test scores
lb.add_score("Alice", "Math Quiz", 5, 5)
lb.add_score("Bob", "Geography Quiz", 3, 5)
lb.add_score("Alice", "Science Quiz", 4, 5)

# Display leaderboard
print(lb.display_leaderboard(10))

# Get user history
print("\nAlice's history:")
for entry in lb.get_user_history("Alice"):
    print(f"  {entry['quiz_title']}: {entry['score']}/{entry['total']} ({entry['percentage']:.1f}%)")
PYEOF
```

### 4. Test Utilities
```bash
python << 'PYEOF'
from src.utils.shuffle import shuffle_options
from src.utils.analytics import QuizAnalytics
from src.utils.timer import CountdownTimer

# Test shuffle
options = ["Paris", "London", "Berlin", "Rome"]
shuffled, new_answer = shuffle_options(options, "A")
print(f"Original: {options}")
print(f"Shuffled: {shuffled}")
print(f"New answer letter: {new_answer}")

# Test analytics
results = [
    {"is_correct": True, "difficulty": "easy"},
    {"is_correct": True, "difficulty": "easy"},
    {"is_correct": False, "difficulty": "hard"},
]
analytics = QuizAnalytics(results)
print(f"\nAnalytics:\n{analytics.summary()}")

# Test timer
timer = CountdownTimer(3)
timer.start()
import time
time.sleep(1)
print(f"Time remaining: {timer.get_remaining()}s")
PYEOF
```

### 5. Test CLI UI (Interactive Menu)
```bash
python -m src.main
```

This starts the full interactive menu. You can:
- Generate quiz by topic
- Generate quiz by difficulty
- View leaderboard
- View your history
- Choose to run quizzes interactively

## Testing Scenarios

### Scenario 1: Basic Quiz Generation & Running
1. Start the app: `python -m src.main`
2. Select "Generate Quiz by Topic"
3. Choose "Geography"
4. Set 2 questions
5. Name it "My Test"
6. Run the quiz
7. Answer A, B, C, or D when prompted
8. View your score

### Scenario 2: Create Multiple Quizzes & Check Leaderboard
```bash
python << 'PYEOF'
from src.creators.quiz_creator import QuizCreator
from src.runners.quiz_runner import QuizRunner
from src.utils.leaderboard_handler import LeaderboardHandler
from src.config import LEADERBOARD_FILE

creator = QuizCreator()
lb = LeaderboardHandler(LEADERBOARD_FILE)

topics = creator.get_available_categories()[:3]

for topic in topics:
    quiz = creator.create_quiz_by_topic(f"{topic} Quiz", topic, count=2)
    print(f"Created {topic} quiz")
    # Simulate a perfect score
    lb.add_score("TestUser", quiz.title, len(quiz.questions), len(quiz.questions))

# Show results
print("\n" + lb.display_leaderboard())
PYEOF
```

### Scenario 3: Test Adaptive Engine
```bash
python << 'PYEOF'
from src.runners.adaptive_engine import AdaptiveEngine

engine = AdaptiveEngine(success_threshold=0.7)

# Simulate 5 correct answers
for i in range(5):
    engine.log_result({"is_correct": True, "difficulty": "easy"})

print("Should increase difficulty:", engine.should_increase_difficulty())

# Simulate 2 wrong answers (60% = just below threshold)
engine.log_result({"is_correct": False, "difficulty": "easy"})
engine.log_result({"is_correct": False, "difficulty": "easy"})

print("Recent performance:", engine.get_performance_summary())
PYEOF
```

### Scenario 4: Test File Handling
```bash
python << 'PYEOF'
from src.utils.file_handler import load_json, save_json
from pathlib import Path

# Create test data
test_data = [
    {"name": "Test1", "score": 100},
    {"name": "Test2", "score": 85},
]

# Save
test_path = Path("data/test_file.json")
save_json(test_path, test_data)
print(f"Saved to {test_path}")

# Load
loaded = load_json(test_path)
print(f"Loaded: {loaded}")

# Clean up
test_path.unlink()
PYEOF
```

## Edge Cases to Test

1. **No questions for topic**: Try a topic that doesn't exist
2. **Invalid input**: Enter non-letter answers in quiz
3. **Skip/Quit**: Type "skip" or "quit" during quiz
4. **Timer expiration**: Set timer per question and wait
5. **Empty leaderboard**: Check leaderboard before any scores
6. **Difficulty not found**: Try creating quiz with unavailable difficulty

## Performance Testing

Test with large number of quizzes:
```bash
python << 'PYEOF'
import time
from src.creators.quiz_creator import QuizCreator

creator = QuizCreator()
start = time.time()

for i in range(10):
    quiz = creator.create_quiz_by_topic(f"Quiz {i}", "Geography", count=5)
    creator.save_quiz(quiz)

elapsed = time.time() - start
print(f"Created and saved 10 quizzes in {elapsed:.2f} seconds")
PYEOF
```

## Debugging Tips

- Check log files in `data/leaderboard.json` for score history
- View generated quizzes in `data/quizzes/` directory
- Run with `python -c` for quick single-command tests
- Use `pytest -s` to see print statements during tests
- Check `exports/` for PDF exports (if implemented)

