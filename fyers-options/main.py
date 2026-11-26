from fyers_apiv3.FyersWebsocket import data_ws

def onmessage(message):
    """
    Callback function to handle incoming messages from the FyersDataSocket WebSocket.
    """
    print("Response:", message)

def onerror(message):
    """
    Callback function to handle WebSocket errors.
    """
    print("Error:", message)

def onclose(message):
    """
    Callback function to handle WebSocket connection close events.
    """
    print("Connection closed:", message)

def onopen(fyers):
    """
    Callback function to subscribe to data type and symbols upon WebSocket connection.
    """
    data_type = "SymbolUpdate"
    symbols = ["NSE:NIFTY50-INDEX", "NSE:NIFTYBANK-INDEX"]
    fyers.subscribe(symbols=symbols, data_type=data_type)
    fyers.keep_running()

from config import need

access_token = need("FYERS_ACCESS_TOKEN")

# Create a FyersDataSocket instance with the provided parameters
fyers = data_ws.FyersDataSocket(
    access_token=access_token,
    log_path="",
    litemode=False,
    write_to_file=False,
    reconnect=True,
    on_connect=lambda: onopen(fyers),
    on_close=onclose,
    on_error=onerror,
    on_message=onmessage
)

# Establish a connection to the Fyers WebSocket
fyers.connect()
