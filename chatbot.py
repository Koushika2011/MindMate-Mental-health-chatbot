import os
from dotenv import load_dotenv
from groq import Groq

# Load the .env file
load_dotenv()

# Get API key from environment
groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)

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

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="llama3-8b-8192",  # fastest model from Groq
        temperature=0.7,
        max_tokens=200,
    )

    return chat_completion.choices[0].message.content.strip()

# Example loop
if __name__ == "__main__":
    print("💬 Mental Health Checker (Powered by Groq LLaMA 3)\nType 'exit' to quit.")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = analyze_mental_health(user_input)
        print(f"\n🧠 {response}")
