from fyers_apiv3.FyersWebsocket import data_ws
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import sys
import traceback  # For detailed error logging

from config import need, get

access_token = need("FYERS_ACCESS_TOKEN")

# Define the scope and credentials for Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(get("GOOGLE_SERVICE_ACCOUNT", "serviceAccount.json"), scope)
client = gspread.authorize(creds)

# Variable to store the last received data
last_data = {}

# Expected symbols to subscribe
expected_symbols = [
    "NSE:RELIANCE-EQ",
    "NSE:TCS-EQ",
    "NSE:HDFCBANK-EQ",
    "NSE:INFY-EQ",
    "NSE:ICICIBANK-EQ",
    "NSE:KOTAKBANK-EQ",
    "NSE:LT-EQ",
    "NSE:AXISBANK-EQ",
    "NSE:ITC-EQ",
    "NSE:SBIN-EQ",
    "NSE:HCLTECH-EQ",
    "NSE:WIPRO-EQ",
    "NSE:BAJAJFINSV-EQ",
    "NSE:BAJFINANCE-EQ",
    "NSE:TECHM-EQ",
    "NSE:ASIANPAINT-EQ",
    "NSE:NESTLEIND-EQ",
    "NSE:M&M-EQ",
    "NSE:ONGC-EQ",
    "NSE:ULTRACEMCO-EQ",
    "NSE:TITAN-EQ",
    "NSE:UPL-EQ",
    "NSE:IOC-EQ",
    "NSE:MARUTI-EQ",
    "NSE:POWERGRID-EQ",
    "NSE:DRREDDY-EQ",
    "NSE:COALINDIA-EQ"
]

received_symbols = set()  # Track received symbols

# FyersDataSocket instance
fyers = None

# Variable to track if headers are already written
headers_written = False

def onmessage(message):
    """
    Callback function to handle incoming messages from the FyersDataSocket WebSocket.
    """
    global received_symbols
    global last_data
    print("Response:", message)

    if message.get('symbol') in expected_symbols:
        symbol = message.get('symbol')
        ltp = message.get('ltp')
        prev_close = message.get('prev_close_price')
        high_price = message.get('high_price')
        low_price = message.get('low_price')
        
        # Example structure for data to be written
        data = [
            [symbol, ltp, prev_close, high_price, low_price]
        ]
        
        print(f"Response for data: {data}")
        
        write_to_google_sheet(data)

        # Track received symbols
        received_symbols.add(symbol)

        # Check if all expected symbols have been received
        if received_symbols == set(expected_symbols):
            print("All expected symbols received. Exiting...")
            close_connections_and_exit()

def onerror(message):
    """
    Callback function to handle WebSocket errors.
    """
    print("Error:", message)
    traceback.print_exc()  # Print detailed traceback for debugging

def onclose(message):
    """
    Callback function to handle WebSocket connection close events.
    """
    print("Connection closed:", message)

def onopen(fyers_instance):
    """
    Callback function to subscribe to data type and symbols upon WebSocket connection.
    """
    global fyers
    fyers = fyers_instance
    data_type = "SymbolUpdate"
    symbols = expected_symbols
    fyers.subscribe(symbols=symbols, data_type=data_type)
    fyers.keep_running()

def write_to_google_sheet(data):
    global headers_written
    try:
        # Open an existing Google Sheet by name
        sheet_name = get("SHEET_NAME", "FyersAPI")
        sheet = client.open(sheet_name).sheet1
        
        if not headers_written:
            # Prepare headers and write them if not already written
            headers = ["Symbol", "LTP", "Prev Close", "High Price", "Low Price"]
            sheet.append_row(headers)
            headers_written = True
        
        # Write data to the sheet
        for row in data:
            sheet.append_row(row)

        print("Data successfully written to Google Sheet.")

    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()  # Print detailed traceback for debugging

def close_connections_and_exit():
    try:
        global fyers
        # Close WebSocket connection
        if fyers:
            fyers.close()
        
        # Exit the script
        sys.exit()

    except Exception as e:
        print(f"Error closing connections and exiting: {e}")
        sys.exit(1)

def main():
    try:
        # Create a FyersDataSocket instance with the provided parameters
        fyers_instance = data_ws.FyersDataSocket(
            access_token=access_token,
            log_path="",
            litemode=False,
            write_to_file=False,
            reconnect=True,
            on_connect=lambda: onopen(fyers_instance),
            on_close=onclose,
            on_error=onerror,
            on_message=onmessage
        )

        # Establish a connection to the Fyers WebSocket
        fyers_instance.connect()

    except Exception as e:
        print(f"Error connecting to Fyers WebSocket: {e}")
        traceback.print_exc()  # Print detailed traceback for debugging
        sys.exit(1)

if __name__ == "__main__":
    main()
