import mysql.connector
from datetime import datetime, timedelta

def get_monthly_emotion_summary(user_id):
    # Connect to MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="mental_health_chatbot"
    )
    cursor = conn.cursor()

    # Date range for last 30 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    query = """
        SELECT emotion, COUNT(*) 
        FROM chat_history
        WHERE user_id = %s AND timestamp BETWEEN %s AND %s
        GROUP BY emotion
    """
    cursor.execute(query, (user_id, start_date, end_date))
    results = cursor.fetchall()

    conn.close()

    # Format results
    if not results:
        return "No chat data found for this month."

    summary = f"Monthly Emotion Summary ({start_date.date()} to {end_date.date()}):\n"
    for emotion, count in results:
        summary += f"- {emotion}: {count} times\n"
    return summary

if __name__ == "__main__":
    user_id = 1  # Replace with actual user ID
    print(get_monthly_emotion_summary(user_id))
