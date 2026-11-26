import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time

from config import need, get

access_token = need("FYERS_ACCESS_TOKEN")
app_id = need("FYERS_CLIENT_ID")
symbol = "NSE:RELIANCE"  # Replace with the symbol of your choice

# Fetch option chain data
def fetch_option_chain(symbol, expiry, retries=3, delay=5):
    url = f"https://api.fyers.in/v7/quotes/{symbol}?expiry={expiry}"
    headers = {"Authorization": f"{app_id}:{access_token}"}
    for _ in range(retries):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            try:
                data = response.json()
                return data['option_chain']
            except requests.exceptions.JSONDecodeError:
                print("Error decoding JSON response")
                print(response.text)
                return None
        elif response.status_code == 503:
            print("Service unavailable. Retrying...")
            time.sleep(delay)
        else:
            print(f"Failed to fetch data: {response.status_code}")
            print(response.text)
            return None
    print("Failed to fetch data after retries")
    return None

# Parse the data and create a DataFrame
def parse_option_chain_data(data):
    ce_data = data['CE']
    pe_data = data['PE']
    
    ce_df = pd.DataFrame(ce_data)
    pe_df = pd.DataFrame(pe_data)
    
    combined_df = pd.merge(ce_df, pe_df, on='strikePrice', suffixes=('_CE', '_PE'))
    return combined_df

# Plot the data
def plot_oi_vs_strike_price(df):
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='strikePrice', y='openInterest_CE', data=df, label='Call OI')
    sns.lineplot(x='strikePrice', y='openInterest_PE', data=df, label='Put OI')
    plt.xlabel('Strike Price')
    plt.ylabel('Open Interest')
    plt.title('Strike Price vs Open Interest')
    plt.legend()
    plt.grid(True)
    plt.show()

# Example usage
expiry = "2024-07-31"  # Replace with the desired expiry date
option_chain_data = fetch_option_chain(symbol, expiry)

if option_chain_data:
    df = parse_option_chain_data(option_chain_data)
    plot_oi_vs_strike_price(df)
else:
    print("Failed to retrieve option chain data.")
