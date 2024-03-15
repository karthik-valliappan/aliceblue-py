import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pya3 import *
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
sheet = spreadsheet.worksheet("profile")

# Assuming that fields are in the first row
sheet.append_row(fields)

# Get your profile
profile = alice.get_profile()

# Prepare the data
data = [profile[field] if field != 'product' else ', '.join(profile[field]) for field in fields]

# Append the data
sheet.append_row(data)