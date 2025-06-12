import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("TelegramTasks").sheet1  # replace with your actual sheet name

def log_message(username, message, tasks):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([timestamp, username, message, ", ".join(tasks)])
