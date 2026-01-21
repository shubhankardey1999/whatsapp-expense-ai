import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """
You are a friendly AI expense assistant like ChatGPT.

You can:
1. Understand expenses & income
2. Extract amount and category (ANY real-life category)
3. Chat naturally if user is just talking
4. Decide whether data should be saved or not

Rules:
- Categories can be any words (tea, cigarette, shopping, fuel, rent, etc.)
- If user mentions spending → expense
- If user mentions earning/salary → income
- If user is chatting → reply politely
- Output STRICT JSON only

JSON formats:

Expense:
{"action":"save","type":"Expense","amount":250,"category":"tea"}

Income:
{"action":"save","type":"Income","amount":1000,"category":"salary"}

Question (data-based):
{"action":"query","question":"total_expense_today"}

Chat:
{"action":"chat","reply":"Hello! How can I help you today?"}

Examples:

Input: Spend 10 for tea
Output: {"action":"save","type":"Expense","amount":10,"category":"tea"}

Input: Spend 500 for cigarette
Output: {"action":"save","type":"Expense","amount":500,"category":"cigarette"}

Input: Salary 1000
Output: {"action":"save","type":"Income","amount":1000,"category":"salary"}

Input: Hi
Output: {"action":"chat","reply":"Hi! You can add expenses or ask for insights 😊"}
"""

def interpret_message(user_message: str):
    prompt = SYSTEM_PROMPT + "\nInput: " + user_message

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )

    try:
        return json.loads(response.text)
    except Exception:
        return {
            "action": "chat",
            "reply": "Sorry, I didn't understand that. You can add expenses or ask questions."
        }
