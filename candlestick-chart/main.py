import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import mplfinance as mpf

# Read the CSV data from the file
file_path = 'nse-historical-data.csv'
df = pd.read_csv(file_path, sep='\t', thousands=',')

# Print the column names to check if 'Date' is present
print(df.columns)

# Convert the 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'], format='%b %d, %Y')

# Selecting one month of data (adjust as needed)
one_month_data = df[df['Date'] >= df['Date'].max() - pd.DateOffset(months=1)]

# Prepare the data for mplfinance
mpl_data = one_month_data[['Date', 'Open', 'High', 'Low', 'Price']]  # Assuming 'Price' as a substitute for 'Close'

# Plotting using Seaborn for styling
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))

# Create the candlestick chart
mpf.plot(mpl_data, type='candle', style='yahoo', volume=True)

plt.title('Candlestick Chart - One Month Data')
plt.show()
