"""Streamlit app for Quiz Generator."""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

from src.creators.quiz_creator import QuizCreator
from src.runners.quiz_runner import QuizRunner
from src.utils.leaderboard_handler import LeaderboardHandler
from src.utils.analytics import QuizAnalytics
from src.config import LEADERBOARD_FILE

# Page config
st.set_page_config(
    page_title="Quiz Generator",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state
if "creator" not in st.session_state:
    st.session_state.creator = QuizCreator()
if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = LeaderboardHandler(LEADERBOARD_FILE)
if "username" not in st.session_state:
    st.session_state.username = ""
if "current_quiz" not in st.session_state:
    st.session_state.current_quiz = None
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
if "current_question_idx" not in st.session_state:
    st.session_state.current_question_idx = 0
if "quiz_results" not in st.session_state:
    st.session_state.quiz_results = []
if "quiz_finished" not in st.session_state:
    st.session_state.quiz_finished = False

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5em;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1em;
    }
    .quiz-card {
        background-color: #f0f4f8;
        padding: 1.5em;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1em 0;
    }
    .score-card {
        background-color: #d4edda;
        padding: 1em;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
    }
    .error-card {
        background-color: #f8d7da;
        padding: 1em;
        border-radius: 10px;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)


def render_home():
    """Render home page."""
    st.markdown('<div class="main-header">📝 Quiz Generator</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
        st.subheader("👤 Welcome!")
        username = st.text_input("Enter your name:", value=st.session_state.username, key="home_username")
        if username:
            st.session_state.username = username
            st.success(f"Hello, {username}! 👋")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
        st.subheader("📊 Quick Stats")
        if st.session_state.username:
            history = st.session_state.leaderboard.get_user_history(st.session_state.username)
            st.metric("Quizzes Taken", len(history))
            if history:
                scores = [h["percentage"] for h in history]
                st.metric("Avg Score", f"{sum(scores) / len(scores):.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)


def render_create_quiz():
    """Render quiz creation page."""
    st.markdown('<div class="main-header">🎯 Create Quiz</div>', unsafe_allow_html=True)
    
    # Debug: Show available questions by topic
    with st.expander("📊 Available Questions by Topic"):
        topic_counts = {}
        for q in st.session_state.creator.questions:
            topic = q.topic if q.topic else "Unknown"
            topic_counts[topic] = topic_counts.get(topic, 0) + 1
        
        for topic, count in sorted(topic_counts.items()):
            st.write(f"**{topic}**: {count} questions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Generate by Topic")
        categories = st.session_state.creator.get_available_categories()
        if categories:
            topic = st.selectbox("Select Topic:", categories, key="topic_select")
            count = st.slider("Number of Questions:", 1, 20, 5, key="topic_count")
            title = st.text_input("Quiz Title:", value=f"{topic} Quiz", key="topic_title")
            
            if st.button("📚 Create Quiz by Topic", key="create_topic"):
                if not st.session_state.username:
                    st.error("Please enter your name first (on Home page)")
                else:
                    try:
                        quiz = st.session_state.creator.create_quiz_by_topic(title, topic, count)
                        st.session_state.current_quiz = quiz
                        st.session_state.quiz_started = False
                        st.session_state.current_question_idx = 0
                        st.success(f"✓ Quiz created: {title}")
                        st.info(f"📋 {len(quiz.questions)} questions selected")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        else:
            st.warning("No topics available")
    
    with col2:
        st.subheader("Generate by Difficulty")
        difficulties = st.session_state.creator.get_available_difficulties()
        if difficulties:
            difficulty = st.selectbox("Select Difficulty:", difficulties, key="diff_select")
            count = st.slider("Number of Questions:", 1, 20, 5, key="diff_count")
            title = st.text_input("Quiz Title:", value=f"{difficulty.capitalize()} Quiz", key="diff_title")
            
            if st.button("⚡ Create Quiz by Difficulty", key="create_diff"):
                if not st.session_state.username:
                    st.error("Please enter your name first (on Home page)")
                else:
                    try:
                        quiz = st.session_state.creator.create_quiz_by_difficulty(title, difficulty, count)
                        st.session_state.current_quiz = quiz
                        st.session_state.quiz_started = False
                        st.session_state.current_question_idx = 0
                        st.success(f"✓ Quiz created: {title}")
                        st.info(f"📋 {len(quiz.questions)} questions selected")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        else:
            st.warning("No difficulties available")
    
    # Show created quiz
    if st.session_state.current_quiz:
        st.divider()
        st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
        st.subheader(f"📋 {st.session_state.current_quiz.title}")
        st.write(f"**Category:** {st.session_state.current_quiz.category or 'General'}")
        st.write(f"**Difficulty:** {st.session_state.current_quiz.difficulty}")
        st.write(f"**Questions:** {len(st.session_state.current_quiz.questions)}")
        st.markdown('</div>', unsafe_allow_html=True)


def render_run_quiz():
    """Render quiz runner page."""
    if not st.session_state.username:
        st.warning("⚠️ Please enter your name first (Home page)")
        return
    
    if not st.session_state.current_quiz:
        st.info("ℹ️ Create a quiz first on the 'Create Quiz' page")
        return
    
    quiz = st.session_state.current_quiz
    
    # Quiz header
    st.markdown('<div class="main-header">🎮 Run Quiz</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="quiz-card"><h3>{quiz.title}</h3></div>', unsafe_allow_html=True)
    
    # Progress bar
    progress = st.session_state.current_question_idx / len(quiz.questions)
    st.progress(progress)
    st.write(f"Question {st.session_state.current_question_idx + 1} of {len(quiz.questions)}")
    
    if st.session_state.quiz_finished:
        render_quiz_results()
        return
    
    # Current question
    if st.session_state.current_question_idx < len(quiz.questions):
        question = quiz.questions[st.session_state.current_question_idx]
        
        # Show topic and difficulty
        col_topic, col_diff = st.columns(2)
        with col_topic:
            st.caption(f"📚 Topic: {question.topic}")
        with col_diff:
            st.caption(f"⚡ Difficulty: {question.difficulty}")
        
        st.subheader(f"Q{st.session_state.current_question_idx + 1}: {question.text}")
        
        # Display options
        options_dict = {chr(ord("A") + i): opt for i, opt in enumerate(question.options)}
        selected = st.radio(
            "Choose your answer:",
            options=list(options_dict.keys()),
            format_func=lambda x: f"{x}. {options_dict[x]}",
            key=f"question_{st.session_state.current_question_idx}"
        )
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("⏭️ Next", key="next_btn"):
                is_correct = selected == question.answer
                st.session_state.quiz_results.append({
                    "index": st.session_state.current_question_idx + 1,
                    "question": question.text,
                    "topic": question.topic,
                    "chosen_letter": selected,
                    "chosen_text": options_dict[selected],
                    "correct_letter": question.answer,
                    "is_correct": is_correct,
                    "difficulty": question.difficulty,
                })
                st.session_state.current_question_idx += 1
                
                if st.session_state.current_question_idx >= len(quiz.questions):
                    st.session_state.quiz_finished = True
                st.rerun()
        
        with col2:
            if st.button("⏸️ Save & Exit", key="exit_btn"):
                st.session_state.quiz_started = False
                st.session_state.quiz_finished = False
                st.info("Quiz saved. You can resume later.")
                st.rerun()
        
        with col3:
            if st.button("🔄 Reset Quiz", key="reset_btn"):
                st.session_state.current_question_idx = 0
                st.session_state.quiz_results = []
                st.session_state.quiz_finished = False
                st.info("Quiz reset.")
                st.rerun()


def render_quiz_results():
    """Render quiz results."""
    quiz = st.session_state.current_quiz
    results = st.session_state.quiz_results
    
    analytics = QuizAnalytics(results)
    
    st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
    st.subheader("🎉 Quiz Completed!")
    
    # Score metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Score", f"{analytics.correct_count()}/{analytics.total_questions()}")
    with col2:
        st.metric("Percentage", f"{analytics.percentage_score():.1f}%")
    with col3:
        st.metric("Correct", analytics.correct_count())
    with col4:
        st.metric("Incorrect", analytics.incorrect_count())
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Save score
    if st.button("💾 Save Score to Leaderboard", key="save_score"):
        st.session_state.leaderboard.add_score(
            st.session_state.username,
            quiz.title,
            analytics.correct_count(),
            analytics.total_questions(),
        )
        st.success("✓ Score saved!")
    
    # Detailed results
    st.subheader("📝 Detailed Results")
    for result in results:
        status = "✓" if result["is_correct"] else "✗"
        with st.expander(f"{status} Q{result['index']} ({result.get('topic', 'Unknown')}): {result['question'][:50]}..."):
            st.write(f"**Topic:** {result.get('topic', 'Unknown')}")
            st.write(f"**Difficulty:** {result['difficulty']}")
            st.write(f"**Your answer:** {result['chosen_letter']} ({result['chosen_text']})")
            st.write(f"**Correct answer:** {result['correct_letter']}")
            if not result["is_correct"]:
                st.error("❌ Incorrect")
    
    # Actions
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔙 Back to Home", key="back_home"):
            st.session_state.current_quiz = None
            st.session_state.quiz_finished = False
            st.session_state.current_question_idx = 0
            st.session_state.quiz_results = []
            st.rerun()
    
    with col2:
        if st.button("🔄 Take Another Quiz", key="another_quiz"):
            st.session_state.quiz_finished = False
            st.session_state.current_question_idx = 0
            st.session_state.quiz_results = []
            st.rerun()


def render_leaderboard():
    """Render leaderboard page."""
    st.markdown('<div class="main-header">🏆 Leaderboard</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top Scores")
        leaderboard_data = st.session_state.leaderboard.get_leaderboard(10)
        
        if leaderboard_data:
            df = pd.DataFrame(leaderboard_data)
            df = df[["username", "quiz_title", "score", "total", "percentage"]].copy()
            df.columns = ["User", "Quiz", "Score", "Total", "%"]
            df = df.reset_index(drop=True)
            df.index = df.index + 1
            
            st.dataframe(df, use_container_width=True)
            
            # Chart
            top_users = df.groupby("User")["%"].mean().nlargest(5)
            fig = go.Figure(data=[
                go.Bar(x=top_users.index, y=top_users.values, marker_color="lightblue")
            ])
            fig.update_layout(
                title="Top 5 Users (Avg Score)",
                xaxis_title="User",
                yaxis_title="Average %",
                height=400,
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No scores yet. Start taking quizzes!")
    
    with col2:
        if st.session_state.username:
            st.subheader(f"📊 {st.session_state.username}'s History")
            user_history = st.session_state.leaderboard.get_user_history(st.session_state.username)
            
            if user_history:
                df_user = pd.DataFrame(user_history)
                df_user = df_user[["quiz_title", "score", "total", "percentage"]].copy()
                df_user.columns = ["Quiz", "Score", "Total", "%"]
                df_user = df_user.reset_index(drop=True)
                df_user.index = df_user.index + 1
                
                st.dataframe(df_user, use_container_width=True)
                
                # User chart
                fig_user = go.Figure(data=[
                    go.Scatter(
                        x=list(range(len(user_history))),
                        y=[h["percentage"] for h in user_history],
                        mode="lines+markers",
                        name="Score %",
                        marker=dict(size=10, color="green"),
                        line=dict(width=2),
                    )
                ])
                fig_user.update_layout(
                    title=f"{st.session_state.username}'s Progress",
                    xaxis_title="Quiz #",
                    yaxis_title="Score %",
                    height=400,
                )
                st.plotly_chart(fig_user, use_container_width=True)
            else:
                st.info("No quizzes completed yet.")
        else:
            st.info("👤 Enter your name on the Home page to see your history.")


# Sidebar navigation
st.sidebar.markdown("# 📚 Quiz Generator")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate:",
    ["🏠 Home", "🎯 Create Quiz", "🎮 Run Quiz", "🏆 Leaderboard"],
    label_visibility="collapsed",
)

st.sidebar.markdown("---")
st.sidebar.subheader("ℹ️ About")
st.sidebar.info(
    "A comprehensive quiz application with topic filtering, "
    "difficulty levels, leaderboard, and adaptive testing."
)

# Route pages
if page == "🏠 Home":
    render_home()
elif page == "🎯 Create Quiz":
    render_create_quiz()
elif page == "🎮 Run Quiz":
    render_run_quiz()
elif page == "🏆 Leaderboard":
    render_leaderboard()
