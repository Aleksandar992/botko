import pandas as pd
import matplotlib.pyplot as plt
from pandas_datareader import data as web

# Make function for calls to Yahoo Finance
def get_adj_close(ticker, start, end):
    start = start
    end = end
    info = web.DataReader(ticker, data_source='yahoo', start=start, end=end)['Adj Close']
    return pd.DataFrame(info)

# Get Adjusted Closing Prices for BTC_USD
BTC_USD = get_adj_close('BTC-USD', '2/16/2018', '9/16/2018')

# set number of days and standard deviations to use for rolling 
# lookback period for Bollinger band calculation
window = 30
no_of_std = 2

# calculate rolling mean and standard deviation
rolling_mean = BTC_USD['Adj Close'].rolling(window).mean()
rolling_std = BTC_USD['Adj Close'].rolling(window).std()

# create two new DataFrame columns to hold values of upper and lower Bollinger bands
BTC_USD['30 Day MA'] = rolling_mean
BTC_USD['Upper Band'] = rolling_mean + (rolling_std * no_of_std)
BTC_USD['Lower Band'] = rolling_mean - (rolling_std * no_of_std)

# Simple 30 Day Bollinger Band for Facebook (2016-2017)
BTC_USD[['Adj Close', '30 Day MA', 'Upper Band', 'Lower Band']].plot(figsize=(12,6))
plt.title('30 Day Bollinger Band for Bitcoin')
plt.ylabel('Price (USD)')
plt.show()

BTC_USD['Position'] = None

# fill our position column based on the following rules:
#     * set to short (-1) when the price hits the upper band
#     * set to long (1) when it hits the lower band       
mode = 'open'
for index in range(len(BTC_USD)):
    if index == 0:
        continue

    row = BTC_USD.iloc[index]
    prev_row = BTC_USD.iloc[index - 1]

    # long?
    if mode == 'open' and row['Adj Close'] < row['Lower Band'] and prev_row['Adj Close'] > prev_row['Lower Band']:
        BTC_USD.iloc[index, BTC_USD.columns.get_loc('Position')] = 1
        mode = 'close'

    # short?
    if mode == 'close' and row['Adj Close'] > row['Upper Band'] and prev_row['Adj Close'] < prev_row['Upper Band']:
        BTC_USD.iloc[index, BTC_USD.columns.get_loc('Position')] = -1
        mode = 'open'

BTC_USD.dropna(subset=['Position'])

BTC_USD[['Adj Close', '30 Day MA', 'Upper Band','Lower Band']].plot(figsize=(14, 7))

for index, pos in BTC_USD.dropna(subset=['Position'])['Position'].iteritems():
    plt.axvline(index, color='green' if pos == 1 else 'red')
plt.show()




