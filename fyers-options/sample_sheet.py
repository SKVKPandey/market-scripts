import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Define the scope and credentials for Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("serviceAccount.json", scope)
client = gspread.authorize(creds)

def open_and_write_to_sheet(sheet_name):
    try:
        # Open an existing Google Sheet by name
        sheet = client.open(sheet_name).sheet1
        print(f"Opened sheet: '{sheet_name}'")

        # Sample data to write
        data = [
            ["Name", "Age", "City"],
            ["John Doe", 30, "New York"],
            ["Jane Smith", 25, "San Francisco"],
            ["Michael Brown", 35, "Chicago"]
        ]

        # Write data to the sheet
        for row in data:
            sheet.append_row(row)

        print("Sample data successfully written to Google Sheet.")

    except Exception as e:
        print(f"Error: {e}")

def main():
    sheet_name = "FyersAPI"  # Replace with your existing sheet name
    open_and_write_to_sheet(sheet_name)

if __name__ == "__main__":
    main()
