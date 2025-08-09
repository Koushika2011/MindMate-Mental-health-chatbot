import mysql.connector
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
def save_chat(username, message, emotion, analysis_result):
    conn = get_connection()
    cursor = conn.cursor()
    timestamp = datetime.now()

    query = """
        INSERT INTO chat_logs (username, message, emotion, analysis_result, timestamp)
        VALUES (%s, %s, %s, %s, %s)
    """
    values = (username, message, emotion, analysis_result, timestamp)
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()
def get_emotion_stats(username, period="weekly"):
    conn = get_connection()
    cursor = conn.cursor()

    if period == "weekly":
        query = """
        SELECT emotion, COUNT(*) as count
        FROM chat_logs
        WHERE username = %s AND timestamp >= NOW() - INTERVAL 7 DAY
        GROUP BY emotion
        """
    elif period == "monthly":
        query = """
        SELECT emotion, COUNT(*) as count
        FROM chat_logs
        WHERE username = %s AND timestamp >= NOW() - INTERVAL 30 DAY
        GROUP BY emotion
        """
    else:
        return None

    cursor.execute(query, (username,))
    results = cursor.fetchall()
    conn.close()

    if results:
        # Convert to dictionary
        return {emotion: count for emotion, count in results}
    return None
