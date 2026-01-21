import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

import json
import os

creds_json = json.loads(os.environ["GOOGLE_CREDS"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(
    creds_json, scope

)

client = gspread.authorize(creds)
sheet = client.open("expense_tracker").worksheet("Sheet1")


def save_record(record_type, amount, category):
    now = datetime.now()

    sheet.append_row([
        now.strftime("%Y-%m-%d"),
        record_type,
        int(amount),
        category.lower(),
        now.strftime("%B"),
        now.year
    ])
