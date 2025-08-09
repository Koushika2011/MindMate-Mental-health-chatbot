import os
import streamlit as st
import mysql.connector
from datetime import datetime
from dotenv import load_dotenv
from transformers import pipeline
from groq import Groq
from auth.auth import create_user, login_user
from db.database import get_connection, save_chat  # Updated import
from db.database import get_emotion_stats


# Sidebar Menu
menu = ["Login", "Signup"]
choice = st.sidebar.selectbox("Account", menu)

# Auth state
if "auth" not in st.session_state:
    st.session_state.auth = False
    st.session_state.user = ""

# Signup
if choice == "Signup":
    st.title("Signup")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type='password')
    if st.button("Create Account"):
        if create_user(username, email, password):
            st.success("Account created! You can now log in.")
        else:
            st.error("Username already exists or error occurred.")

# Login
elif choice == "Login":
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        if login_user(username, password):
            st.session_state.auth = True
            st.session_state.user = username
            st.success(f"Welcome back, {username}!")
        else:
            st.error("Invalid credentials")

# Block access if not logged in
if not st.session_state.auth:
    st.warning("Please log in to use the chatbot.")
    st.stop()

# Load environment & Groq client
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)

emotion_classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=1,
    device=-1  # Explicitly set to CPU
)

emotion_to_emoji = {
    "joy": "😃", "sadness": "😔", "anger": "😡",
    "fear": "😨", "surprise": "😲", "disgust": "🤢", "neutral": "😐"
}

def detect_emotion(text):
    result = emotion_classifier(text)[0]
    label = result[0]['label'].lower()
    return label.capitalize(), emotion_to_emoji.get(label, "🧠")

def analyze_mental_health(user_message):
    prompt = f"""
You are a compassionate mental health AI assistant. Based on the following user input, identify their most likely mental condition 
from the following options: ["anxiety", "depression", "stress", "normal", "happy", "lonely"]. 

Give a short diagnosis and a kind suggestion.

User message: "{user_message}"

Respond in this format:
Mental State: <state>
Suggestion: <your advice>
"""
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=200
    )
    return response.choices[0].message.content.strip()

# UI
st.title("🧠 Mental Health Checker")
user_input = st.text_area("Describe how you're feeling:")

if user_input:
    emotion, emoji = detect_emotion(user_input)
    st.markdown(f"**Detected Emotion:** {emotion} {emoji}")

if st.button("Analyze"):
    if user_input.strip() != "":
        with st.spinner("Analyzing..."):
            result = analyze_mental_health(user_input)
        st.success("Result:")
        st.markdown(result)

        # Save chat to DB
        save_chat(
            username=st.session_state.user,
            message=user_input,
            emotion=emotion,
            analysis_result=result
        )
    else:
        st.warning("Please enter a message to analyze.")
st.subheader("📊 Your Emotion Trend")
analysis_type = st.selectbox("Select Time Period", ["Weekly", "Monthly"])
if st.button("Show Emotion Stats"):
    period = analysis_type.lower()
    stats = get_emotion_stats(st.session_state.user, period=period)
    
    if stats:
        st.bar_chart(stats)
    else:
        st.info(f"No emotion data found for the last {period}.")