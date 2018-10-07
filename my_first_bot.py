from binance.client import Client
import time
import matplotlib
from matplotlib import cm
import matplotlib.pyplot as plt
from binance.enums import *
from BinanceKeys import BinanceKey1
from time import sleep
import pandas as pd


api_key = BinanceKey1['api_key']
api_secret = BinanceKey1['api_secret']

client = Client('api_key' , 'api_secret', {"verify": False, "timeout": 30})

# deposit address for BTC
address = client.get_deposit_address(asset='BTC')

def run():
    list_of_symbols = ['BTCUSDT', 'ETHUSDT', 'LTCBTC', 'DASHUSDT', 'XMRUSDT']
    time_horizon = "Short"
    Risk_profile = "High"
    print("\n-----------------------------------------------------------------------------------\n")
    print("Hello and Welcome to the Crypto Trader Bot which is called My_First_Bot\nThis Bot is created 2018 by Aleksandar Djordjevic")
    print("This should be a functionality automated trading bot on Binance")
    print("\n-----------------------------------------------------------------------------------\n")
    time.sleep(5)


    # Status of Exchange & Account
    try:
        status = client.get_system_status()
        print("\nClient Status: ", status)

        withdraws = client.get_withdraw_history()
        print("\nClient Withdraw History: ", withdraws)

        info = client.get_exchange_info() # ovde modu da stavim i odredjeni koin npr btc, videti sa urosem sta je bolje
        print("\nExchange Info about client (Limits): ", info)
    except():
        pass

    #test order
    try:
        order = client.create_test_order(
            symbol='LTCBTC',
            side=SIDE_BUY,
            type=ORDER_TYPE_LIMIT,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=100,
            price='0.00001')
    except:
        print("\n ATTENTION: NON-VALID CONNECTION WITH BINANCE \n")

    coin_prices(list_of_symbols)
    coin_tickers(list_of_symbols)
    for symbol in list_of_symbols:
        market_depth(symbol)

 # recent trades
    rec_trades = client.get_recent_trades(symbol='BTCUSDT')
    print("Recent Trades: ", trades)
    print("Local Time: ", time.localtime())
    print("Recent Trades Time: ", convert_time_binance(trades[0]['time']))

    # historical trades
    try:
        hist_trades = client.get_historical_trades(symbol='BTCUSDT')
        print("Historical Trades: ", hist_trades)
    except:
        print('\nATTENTION: NON VALID CONNECTION WITH BINANCE\n')

    # aggregate trades
    agg_trades = client.get_aggregate_trades(symbol='BTCUSDT')
    print("\nAggregate Trades: ", agg_trades)

    save_historical_data.save_historic_klines_csv("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, "1 hours ago UTC", "now UTC")
    save_historical_data.save_historic_klines_csv("BTCUSDT", Client.KLINE_INTERVAL_1WEEK, "12 months ago UTC", "now UTC")
    save_historical_data.save_historic_klines_csv("BTCUSDT", Client.KLINE_INTERVAL_1MONTH, "12 months ago UTC", "now UTC")
    save_historical_data.save_historic_klines_csv("ETHUSDT", Client.KLINE_INTERVAL_5MINUTE, "3 hours ago UTC", "now UTC")
    save_historical_data.save_historic_klines_csv("DASHUSDT", Client.KLINE_INTERVAL_30MINUTE, "1 day ago UTC", "now UTC")
    save_historical_data.save_historic_klines_csv("XMRUSDT", Client.KLINE_INTERVAL_15MINUTE, "8 hours ago UTC", "now UTC")
    save_historical_data.save_historic_klines_csv("ETHBTC", Client.KLINE_INTERVAL_30MINUTE, "1 day ago UTC", "now UTC")
    save_historical_data.save_historic_klines_csv("LTCUSDT", Client.KLINE_INTERVAL_1MINUTE, "1 hours ago UTC", "now UTC")
    save_historical_data.save_historic_klines_csv("XMRUSDT", Client.KLINE_INTERVAL_1MINUTE, "1 hours ago UTC", "now UTC")


def convert_time_binance(gt):
    gt = client.get_server_time()
    print("Binance Time: ", gt)
    print(time.localtime())
    aa = str(gt)
    bb = aa.replace("{'serverTime': ","")
    aa = bb.replace("}","")
    gg=int(aa)
    ff=gg-10799260
    uu=ff/1000
    yy=int(uu)
    tt=time.localtime(yy)
    print(tt)
    return tt

def market_depth(BTCUSDT, num_entries=20):
    a=0     # Asks
    print("Order Book: ", convert_time_binance(client.get_server_time()))
    depth = client.get_order_book(symbol='BTCUSDT')
    print(depth)
    print(depth['asks'][0])
    ask_tot=0.0
    ask_price =[]
    ask_quantity = []
    bid_price = []
    bid_quantity = []
    bid_tot = 0.0
    place_order_ask_price = 0
    place_order_bid_price = 0
    max_order_ask = 0
    max_order_bid = 0
    print("\n", BTCUSDT, "\nDepth     ASKS:\n")
    print("Price     Amount")
    for ask in depth['asks']:
        if a<num_entries:
            if float(ask[1])>float(max_order_ask):
                max_order_ask=ask[1]
                place_order_ask_price=round(float(ask[0]),5)-0.0001
            ask_price.append(float(ask[0]))
            ask_tot+=float(ask[1])
            ask_quantity.append(ask_tot)
            print(ask)
            a+=1
    b=0     # Bids
    print("\n", BTCUSDT, "\nDepth     BIDS:\n")
    print("Price     Amount")
    for bid in depth['bids']:
        if b<num_entries:
            if float(bid[1])>float(max_order_bid):
                max_order_bid=bid[1]
                place_order_bid_price=round(float(bid[0]),5)+0.0001
            bid_price.append(float(bid[0]))
            bid_tot += float(bid[1])
            bid_quantity.append(bid_tot)
            print(bid)
            b+=1
    return ask_price, ask_quantity, bid_price, bid_quantity, place_order_ask_price, place_order_bid_price

def displaying_orders():
    ap, aq, bp, bq, place_ask_order, place_bid_order, spread, proj_spread, max_bid, min_ask = visualize_market_depth(wait, tot_time, coin)
    max_bid = max(bid_pri)
    min_ask = min(ask_pri)
    max_quant = max(ask_quan[-1], bid_quan[-1])
    spread = round(((min_ask-max_bid)/min_ask)*100,5) 
    proj_order_spread = round(((ask_order-bid_order)/ask_order)*100,1)
    price=round(((max_bid+min_ask)/2), precision)
    print("Coin: {}\nSpread: {} %\nProject Spread: {} %\nMax Bid: {}\nMin Ask: {}".format(coin, spread, proj_spread, max_bid, min_ask))

    if spread > 0.05%:
        bid_order1 = client.order_market_buy(
            symbol='BTCUSDT',
            quantity=100)

        ask_order1 = client.order_market_sell(
            symbol='BTCUSDT',
            quantity=100)

    
    if proj_order_spread > 0.05%:
        quant1=100        
        bid_order2 = client.order_limit_buy(
            symbol='BTCUSDT',
            quantity=100,
            price=0.00001)

        ask_order2 = client.order_limit_sell(
            symbol='BTCUSDT',
            quantity=100,
            price=0.00001)


# Ovde treba da odradim vizuelizaciju ako je market_depth dobar


def coin_prices(watch_list):
    prices = client.get_all_tickers()
    print("\nSelected (watch list) Ticker Prices: \n")
    for price in prices:
        if price['symbol'] in watch_list:
            print(price)
    return prices


def coin_tickers(watch_list):
    tickers = client.get_orderbook_tickers()
    print("\nWatch List Order Tickers: \n")
    for tick in tickers:
        if tick['symbol'] in watch_list:
            print(tick)
    return tickers

def portfolio_management(deposit = '1000', withdraw=0, portfolio_amt = '0', portfolio_type='USDT', test_acct='True'):
    pass

def Bollinger_Bands():
    pass
    df[['Coin price','Bollinger High','Bollinger Low']].plot()
    plt.title('Bollinger Band for Cryptocurrency')
    plt.ylabel('Price (USD)')
    plt.xlabe;('Time')
    plt.show()

if __name__ == "__main__":
    run()







