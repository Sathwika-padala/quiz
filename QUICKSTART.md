# 🚀 Quiz Generator - Complete Deployment Guide

## What You Have

A full-stack quiz application with:
- **Backend**: Python quiz logic (creators, runners, analytics)
- **Web Frontend**: Streamlit interactive app
- **Database**: JSON-based leaderboard and quiz storage
- **Testing**: Unit tests and manual testing guides

## Run Locally (Now)

### Option 1: CLI Version (Original)
```bash
python -m src.main
```
Interactive menu in terminal.

### Option 2: Web Version (New - Streamlit)
```bash
streamlit run app.py
```
Then open browser to `http://localhost:8502`

## Deploy to Production (Choose One)

### 🌟 Recommended: Streamlit Cloud (Free & Easy)

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Add Streamlit deployment"
   git push origin main
   ```

2. **Deploy** (30 seconds):
   - Go to https://share.streamlit.io
   - Click "New app"
   - Select your GitHub repo
   - Pick `main` branch and `app.py` file
   - Click "Deploy"

3. **Share**:
   - Your app is now live at: `https://your-username-quiz-app.streamlit.app`

### 🐳 Alternative: Docker (Any Server)

```bash
# Build image
docker build -t quiz-app .

# Run locally
docker run -p 8502:8502 quiz-app

# Deploy to AWS/GCP/Azure (push to container registry)
```

### 🚀 Alternative: Heroku (5 min setup)

```bash
heroku create your-quiz-app
git push heroku main
```

Then access at: `https://your-quiz-app.herokuapp.com`

## Project Structure

```
quiz/
├── app.py                    ← Streamlit web app (START HERE)
├── src/                      ← Core Python modules
│   ├── creators/            ← Quiz creation logic
│   ├── runners/             ← Quiz execution & adaptive engine
│   ├── utils/               ← Utilities (leaderboard, analytics, etc.)
│   ├── models/              ← Data structures
│   └── ui/                  ← CLI interface (original)
├── data/                    ← Questions, leaderboard storage
├── tests/                   ← Unit tests
├── Dockerfile               ← For Docker deployment
├── Procfile                 ← For Heroku deployment
├── requirements.txt         ← Python dependencies
├── DEPLOYMENT.md            ← Full deployment guide
└── STREAMLIT_QUICKSTART.md  ← Streamlit how-to
```

## Features Overview

### 📝 Create Quiz
- Filter by topic (Geography, Chemistry, Math, etc.)
- Filter by difficulty (easy, medium, hard)
- Choose number of questions
- Questions auto-shuffled for randomness

### 🎮 Run Quiz
- Multiple choice questions (A, B, C, D)
- Real-time scoring
- Immediate feedback
- Save results to leaderboard

### 🏆 Leaderboard
- Top scores ranking
- User history tracking
- Performance charts
- Progress visualization

### 📊 Analytics
- Per-user statistics
- Difficulty breakdown
- Score trends over time

## Quick Test

Run this to verify everything works:

```bash
# Test 1: Create quiz
python << 'PYEOF'
from src.creators.quiz_creator import QuizCreator
creator = QuizCreator()
quiz = creator.create_quiz_by_topic("Test", "Math", count=2)
print(f"✓ Quiz created with {len(quiz.questions)} questions")
PYEOF

# Test 2: Run unit tests
pytest tests/ -v

# Test 3: Start Streamlit app
streamlit run app.py
```

## Deployment Checklist

- [x] Backend code (quiz logic) - Complete
- [x] Streamlit web app - Complete  
- [x] Unit tests (8 tests) - All passing ✓
- [x] Sample data - Included
- [x] Configuration - Ready
- [ ] Deploy to Streamlit Cloud - Your turn!
- [ ] Test in browser - Your turn!
- [ ] Share link - Your turn!

## File Locations

| Item | Location |
|------|----------|
| Questions | `data/questions.json` |
| Leaderboard | `data/leaderboard.json` |
| Saved quizzes | `data/quizzes/` |
| Web app | `app.py` |
| Backend code | `src/` |
| Tests | `tests/` |

## Troubleshooting

### Port already in use
```bash
streamlit run app.py --server.port 8503
```

### Module not found
```bash
pip install -r requirements.txt
```

### Leaderboard not showing scores
1. Create a quiz first
2. Run it and answer questions
3. Click "Save Score"
4. Check leaderboard page

## Next Steps

1. **Test locally**: `streamlit run app.py`
2. **Push to GitHub**: `git push`
3. **Deploy on Streamlit Cloud**: Follow link above
4. **Share**: Send your app URL to users
5. **Monitor**: Check usage in Streamlit dashboard

## Support

- **Streamlit Docs**: https://docs.streamlit.io
- **Deployment Help**: See `DEPLOYMENT.md`
- **How to Use**: See `STREAMLIT_QUICKSTART.md`
- **Testing**: See `TESTING.md`

---

**You're all set!** 🎉 Your quiz generator is ready to deploy.
