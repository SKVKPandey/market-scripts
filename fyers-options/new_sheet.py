from config import get, need  # noqa: F401
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Define the scope and credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(get("GOOGLE_SERVICE_ACCOUNT", "serviceAccount.json"), scope)

# Authorize with credentials
client = gspread.authorize(creds)

def create_and_share_sheet(sheet_name):
    # Create a new Google Sheet
    new_sheet = client.create(sheet_name)

    # Share the Google Sheet with edit permissions (can be customized)
    new_sheet.share(need("SHARE_WITH"), perm_type='user', role='writer')

    # Get and print the URL of the created Google Sheet
    sheet_url = new_sheet.url
    print(f"Created Sheet: '{sheet_name}'")
    print(f"Sheet URL: {sheet_url}")

# Example usage
create_and_share_sheet("FyersAPI")
