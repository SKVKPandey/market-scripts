from nsepy import get_history
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def fetch_option_chain(symbol, expiry_date, option_type, strike_price, start_date, end_date):
    """
    Fetches option chain data including OI vs strike price.
    
    Parameters:
        symbol (str): Stock symbol (e.g., 'RELIANCE').
        expiry_date (str): Expiry date of the option (e.g., '2024-07-25').
        option_type (str): Type of option ('CE' for Call, 'PE' for Put).
        strike_price (int): Strike price of the option.
        start_date (str): Start date for fetching data (e.g., '2024-07-01').
        end_date (str): End date for fetching data (e.g., '2024-07-18').

    Returns:
        DataFrame: Option chain data with open interest and strike prices.
    """
    # Convert string dates to datetime objects
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d')
    
    # Fetch option chain data
    data = get_history(symbol=symbol,
                      start=start_date,
                      end=end_date,
                      expiry_date=expiry_date,
                      option_type=option_type,
                      strike_price=strike_price,
                      index=False)
    return data

def plot_oi_vs_strike(data):
    """
    Plots open interest vs strike price.

    Parameters:
        data (DataFrame): Data containing open interest and strike price.
    """
    if data.empty:
        print("No data available for the given parameters.")
        return

    # Group by strike price and sum open interest
    oi_data = data.groupby('Strike Price')['Open Interest'].sum().reset_index()

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(oi_data['Strike Price'], oi_data['Open Interest'], marker='o')
    plt.title('Open Interest vs Strike Price')
    plt.xlabel('Strike Price')
    plt.ylabel('Open Interest')
    plt.grid(True)
    plt.show()

# Example parameters (change if needed)
symbol = 'NIFTY'
expiry_date = '2024-07-25'
option_type = 'CE'  # Call option
strike_price = 18000  # Use a common strike price
start_date = '2024-07-01'
end_date = '2024-07-18'

# Fetch data and plot
option_data = fetch_option_chain(symbol, expiry_date, option_type, strike_price, start_date, end_date)
plot_oi_vs_strike(option_data)
