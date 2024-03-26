import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pya3 import *
from datetime import date

# AliceBlue credentials
username = open('username.txt', 'r').read()
api_key = open('api_key.txt', 'r').read()

# Create an AliceBlue instance
alice = Aliceblue(username, api_key)

# Get the session ID
session_id = alice.get_session_id()['sessionID']

# Use your own JSON file that you downloaded when you created your service account
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('secret.json', scope)
client = gspread.authorize(creds)

# Get the balance data
balance_data = alice.get_balance()

# Open the Google Sheet and get the "Balance" worksheet
spreadsheet = client.open("TradingLiveData")
profile_sheet = spreadsheet.worksheet("Balance")

# Get the headers (first row) of the sheet
headers = profile_sheet.row_values(1)

# Get today's date
today = today = date.today().isoformat()

# Check if data is already updated for today's date
dates = profile_sheet.col_values(headers.index('date') + 1)  # Adding 1 because Google Sheets is 1-indexed
if str(today) in dates:
    print("Data is already updated for today's date.")
else:
    # Iterate over each dictionary in the balance data
    for data in balance_data:
        # Create a new row with the same order as the headers
        new_row = [today if header == 'date' else data.get(header, "") for header in headers]
        # Append the new row to the sheet
        profile_sheet.append_row(new_row)
    print("The Google Sheet has been successfully updated with the balance data.")
