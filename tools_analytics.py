import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", scope
)

client = gspread.authorize(creds)
sheet = client.open("expense_tracker").worksheet("Sheet1")

def load_df():
    return pd.DataFrame(sheet.get_all_records())

def total_expense_today():
    df = load_df()
    today = datetime.now().strftime("%Y-%m-%d")
    total = df[(df["type"] == "Expense") & (df["date"] == today)]["amount"].sum()
    return f"📅 You spent ₹{int(total)} today"

def total_expense_month():
    df = load_df()
    month = datetime.now().strftime("%B")
    total = df[(df["type"] == "Expense") & (df["month"] == month)]["amount"].sum()
    return f"📊 Total expense this month: ₹{int(total)}"
