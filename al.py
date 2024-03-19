import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pya3 import *
from datetime import date


username=open('username.txt','r').read()
api_key=open('api_key.txt','r').read()
alice=Aliceblue(username,api_key)
alice.get_session_id()['sessionID']
get_profile_response=alice.get_profile()
print(alice.get_profile()) # get profile

####### Google Spreadsheet update ########

# Use the same keys you have in your returned dictionary
fields = ['accountStatus', 'dpType', 'accountId', 'sBrokerName', 'product', 'accountName', 'cellAddr', 'emailAddr', 'exchEnabled']

# Use your own JSON file that you downloaded when you created your service account
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('secret.json', scope)
client = gspread.authorize(creds)

# Open the test sheet. Use your own sheet name.
spreadsheet = client.open("TradingLiveData")
profile_sheet = spreadsheet.worksheet("profile")

# Assuming that fields are in the first row
profile_sheet.append_row(fields)

# Get your profile
profile = alice.get_profile()

# Prepare the data
data = [profile[field] if field != 'product' else ', '.join(profile[field]) for field in fields]

# Append the data
profile_sheet.append_row(data)


################### Balance print and summary page to identify the brokerage amount ############

# Open the spreadsheet and select the sheet. Use your own spreadsheet and sheet names.
spreadsheet = client.open("TradingLiveData")
summary_sheet = spreadsheet.worksheet("Summary")

# Get your balance
balance = alice.get_balance()

# Get the net value
net_value = balance[0]['net']

# Get today's date
today = date.today()

# Check if today's date is already in the 'Date' column
dates = summary_sheet.col_values(1)  # Assuming 'Date' is the first column
if str(today) in dates:
    # Find the row with today's date
    row = dates.index(str(today)) + 1  # Adding 1 because gspread row indices start at 1

    # Update the balance
    summary_sheet.update_cell(row, 2, net_value)  # Assuming 'Opening Balance' is the second column
else:
    # Prepare the data
    data = [str(today), net_value]

    # Append the data to the 'Date' and 'Opening Balance' columns
    summary_sheet.append_row(data)