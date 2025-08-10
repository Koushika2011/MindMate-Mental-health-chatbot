MindMate – AI-Powered Mental Health Chatbot
MindMate is an AI-powered mental health chatbot that provides empathetic, context-aware responses while detecting and tracking user emotions over time. It enables self-monitoring through weekly/monthly emotion trend analytics.

🚀 Features
AI-Powered Conversations – Built with Groq LLaMA for real-time, empathetic responses.

Emotion Detection – Uses Hugging Face emotion classification to analyze user input.

Trend Analytics – MySQL integration for storing chats and visualizing mood patterns.

Weekly/Monthly Charts – Streamlit-based dynamic charts for mood tracking.

🛠 Tech Stack
Frontend & UI: Streamlit

Backend & Logic: Python

AI Model: Groq LLaMA

Emotion Classification: Hugging Face Transformers

Database: MySQL

📦 Installation
Clone the repository:

git clone https://github.com/Koushika2011/MindMate-Mental-health-chatbot.git
cd MindMate-Mental-health-chatbot
Install dependencies:

pip install -r requirements.txt
Create a .env file:

GROQ_API_KEY=your_api_key_here
MYSQL_HOST=localhost
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=your_database

Run the app:
streamlit run app.py

📊 Emotion Analytics Example
Tracks user emotions over sessions.

Displays weekly/monthly trends in charts for self-awareness.

📜 License

This project is for educational purposes only. Not intended for medical use.
