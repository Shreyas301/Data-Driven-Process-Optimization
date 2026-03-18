import gspread
from google.oauth2.service_account import Credentials

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file("bold-hallway-452117-j5-0cc3fe0b9b42.json", scopes=scope)

client = gspread.authorize(creds)

sheet = client.open("Order_Process_Data").sheet1

data = sheet.get_all_records()

print(data)
