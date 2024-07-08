import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Define the scope and credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("serviceAccount.json", scope)

# Authorize with credentials
client = gspread.authorize(creds)

# Function to list all available Google Sheets
def list_google_sheets():
    sheets = client.openall()
    for sheet in sheets:
        print(f"Sheet: {sheet.title}, ID: {sheet.id}")

# List all available Google Sheets
list_google_sheets()
