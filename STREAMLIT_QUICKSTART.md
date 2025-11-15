# Streamlit Quick Start Guide

## What is Streamlit?

Streamlit is a Python framework for building interactive web apps without needing HTML/CSS/JavaScript. It's perfect for deploying data apps and dashboards.

## Features of Our Quiz Generator Streamlit App

✅ **Interactive Quiz Creation**
- Select topic or difficulty
- Choose number of questions
- Auto-save quizzes

✅ **Real-time Quiz Running**
- Progressive answer validation
- Immediate feedback
- Score tracking

✅ **Leaderboard & Analytics**
- Top scores ranking
- User history tracking
- Charts and statistics

✅ **Session Persistence**
- User profiles
- Quiz progress saved
- History preserved

## How to Run

### Locally (Development)

```bash
cd /workspaces/quiz
streamlit run app.py
```

Open browser to: `http://localhost:8502`

### Via Docker

```bash
docker build -t quiz-app .
docker run -p 8502:8502 quiz-app
```

### On Streamlit Cloud (Production)

See `DEPLOYMENT.md` for full instructions.

## How to Use the App

### 1. **Home Page** 🏠
   - Enter your username
   - View your quick stats
   - See quizzes taken

### 2. **Create Quiz** 🎯
   - Choose topic or difficulty
   - Select number of questions
   - Give quiz a title
   - Click "Create Quiz"

### 3. **Run Quiz** 🎮
   - Select answer option (A, B, C, D)
   - Click "Next" to continue
   - View results after completion
   - Click "Save Score" to record leaderboard entry

### 4. **Leaderboard** 🏆
   - View top scores worldwide
   - Check your personal history
   - See progress charts

## File Structure

```
app.py                    # Main Streamlit app
.streamlit/config.toml    # Streamlit theme & settings
Procfile                  # Heroku deployment
Dockerfile                # Docker deployment
DEPLOYMENT.md             # Full deployment guide
src/                      # Core modules (unchanged)
data/                     # Data storage
```

## Customize the App

### Change Theme

Edit `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#FF6B6B"  # Your color
backgroundColor = "#F0F2F6"
```

### Modify Layout

Edit `app.py` and change:
- Sidebar items
- Page structure
- Colors and styling

### Add New Pages

```python
def render_new_page():
    st.title("New Page")
    # Your content here

# In routing section:
elif page == "📄 New Page":
    render_new_page()
```

## Deployment Checklist

- [ ] Test locally: `streamlit run app.py`
- [ ] All pages functional
- [ ] Leaderboard working
- [ ] Quiz creation working
- [ ] Quiz running working
- [ ] Push to GitHub
- [ ] Deploy on Streamlit Cloud / Docker
- [ ] Test in production
- [ ] Share URL with users

## Tips & Tricks

### Speed Up Loading
```python
@st.cache_resource
def load_data():
    return QuizCreator()

creator = load_data()
```

### Debug Mode
```bash
streamlit run app.py --logger.level=debug
```

### Clear Cache
```bash
streamlit cache clear
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Port 8502 in use | `streamlit run app.py --server.port 8503` |
| Module not found | `pip install -r requirements.txt` |
| Session state lost | Clear browser cache (CTRL+SHIFT+R) |
| Leaderboard empty | Create and save quiz scores first |
| App slow | Use `@st.cache_resource` for expensive operations |

## Performance

- **Load time**: ~1-2 seconds (local)
- **Quiz interaction**: Real-time (< 100ms)
- **Leaderboard load**: ~500ms (depends on data size)

## Security Notes

- Leaderboard stored in JSON (local)
- For production: migrate to PostgreSQL/MongoDB
- Add authentication if needed
- Validate user input server-side

## Next Steps

1. **Deploy**: Follow DEPLOYMENT.md
2. **Share**: Get your Streamlit URL
3. **Monitor**: Check logs and usage
4. **Iterate**: Add features based on feedback

---

**Questions?** Check `TESTING.md` for programmatic examples and `DEPLOYMENT.md` for advanced setup.
