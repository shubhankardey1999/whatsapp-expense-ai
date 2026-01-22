from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

from agent import interpret_message
from tools_sheets import save_record
from tools_analytics import total_expense_today, total_expense_month

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    msg = request.form.get("Body", "")
    resp = MessagingResponse()

    ai = interpret_message(msg)

    if ai["action"] == "save":
        save_record(ai["type"], ai["amount"], ai["category"])
        reply = f"✅ {ai['type']} added: ₹{ai['amount']} ({ai['category']})"

    elif ai["action"] == "query":
    metric = ai.get("metric")
    period = ai.get("period")

    if metric == "expense" and period == "today":
        reply = total_expense_today()

    elif metric == "expense" and period == "month":
        reply = total_expense_month()

    elif metric == "income" and period == "today":
        reply = total_income_today()

    elif metric == "income" and period == "month":
        reply = total_income_month()

    else:
        reply = "🤔 I can calculate income or expense for today or this month."


    else:
        reply = ai["reply"]

    resp.message(reply)
    return str(resp)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


