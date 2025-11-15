# Streamlit Deployment Guide

## Features

The Streamlit web app includes:

- **🏠 Home Page**: User profile, quick stats, and welcome
- **🎯 Create Quiz**: Generate quizzes by topic or difficulty level
- **🎮 Run Quiz**: Interactive quiz runner with real-time feedback
- **🏆 Leaderboard**: Rankings, charts, and user history tracking

## Local Development

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Locally

```bash
streamlit run app.py
```

The app will open at `http://localhost:8502` (or similar).

## Deployment Options

### Option A: Deploy on Streamlit Cloud (Recommended)

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Add Streamlit app"
   git push origin main
   ```

2. **Go to Streamlit Cloud**: https://share.streamlit.io

3. **Deploy**:
   - Click "New app"
   - Select your GitHub repo
   - Choose branch: `main`
   - Set main file path: `app.py`
   - Click "Deploy"

**Pros**: Free, automatic updates, scalable  
**Cons**: Limited to public repos (or private with paid plan)

### Option B: Deploy on Heroku

1. **Install Heroku CLI**:
   ```bash
   curl https://cli.heroku.com/install.sh | sh
   ```

2. **Create Procfile**:
   ```bash
   echo "web: streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile
   ```

3. **Deploy**:
   ```bash
   heroku login
   heroku create quiz-generator-app
   git push heroku main
   ```

**Pros**: Easy deployment, paid options available  
**Cons**: Costs money for production

### Option C: Deploy on AWS/GCP/Azure

1. **Using Docker** (create `Dockerfile`):
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY . .
   RUN pip install -r requirements.txt
   EXPOSE 8502
   CMD ["streamlit", "run", "app.py", "--server.port=8502", "--server.address=0.0.0.0"]
   ```

2. **Build & Push**:
   ```bash
   docker build -t quiz-generator .
   # Push to container registry and deploy
   ```

**Pros**: Full control, scalable  
**Cons**: More complex setup

### Option D: Deploy on PythonAnywhere

1. Go to https://www.pythonanywhere.com
2. Create account and set up web app
3. Upload code and configure
4. Set Streamlit as the WSGI app

**Pros**: Simple, supports Python  
**Cons**: Limited free tier

## Streamlit Cloud Setup (Simplest)

### Step-by-Step:

1. **Ensure `requirements.txt` is updated**:
   ```bash
   pip freeze > requirements.txt
   ```

2. **Commit and push**:
   ```bash
   git add app.py requirements.txt
   git commit -m "Add Streamlit deployment"
   git push
   ```

3. **Create on Streamlit Cloud**:
   - Visit https://share.streamlit.io
   - Click "New app"
   - Select repo, branch, and file
   - Deploy

4. **Share URL**:
   - Your app will be live at `https://quiz-generator.streamlit.app` (or custom domain)

## Environment Variables (Optional)

For sensitive data, create `.streamlit/secrets.toml`:

```toml
# .streamlit/secrets.toml
db_user = "username"
db_password = "password"
api_key = "your-key"
```

Access in app:
```python
import streamlit as st
username = st.secrets["db_user"]
```

## Performance Tips

1. **Cache data** to avoid reloading:
   ```python
   @st.cache_resource
   def get_creator():
       return QuizCreator()
   ```

2. **Use session state** for faster interactions (already implemented)

3. **Optimize dataframes** with `st.dataframe()` instead of `st.write()`

4. **Lazy load images/data** when needed

## Monitoring

- **Streamlit Cloud Dashboard**: View logs, metrics, and app status
- **Error tracking**: Check `/var/log/streamlit` on self-hosted deployments
- **Performance**: Use `streamlit run app.py --logger.level=debug` locally

## Troubleshooting

### Port already in use
```bash
streamlit run app.py --server.port 8503
```

### Module not found
```bash
pip install -r requirements.txt
```

### Session state issues
- Check browser cache
- Clear with `CTRL+SHIFT+R`

### Data persistence
- Leaderboard stored in `data/leaderboard.json`
- Quizzes stored in `data/quizzes/`
- Use cloud storage for production (AWS S3, Google Cloud Storage)

## Production Checklist

- [ ] Update `requirements.txt` with all dependencies
- [ ] Test app locally: `streamlit run app.py`
- [ ] Check all pages work (Home, Create, Run, Leaderboard)
- [ ] Test quiz creation and running
- [ ] Verify leaderboard saves scores
- [ ] Push to GitHub
- [ ] Deploy on Streamlit Cloud or alternative
- [ ] Test in browser
- [ ] Share link with users

## Post-Deployment

### Monitor Usage
```bash
# Check logs
streamlit logs

# Monitor performance
streamlit run app.py --logger.level=debug
```

### Update App
Just push to GitHub and Streamlit will auto-update (if using Streamlit Cloud).

### Scale Up
- Use Streamlit Sharing for free
- Or upgrade to Streamlit Teams for enterprise features
