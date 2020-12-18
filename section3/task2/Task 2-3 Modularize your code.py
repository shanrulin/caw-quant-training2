#!/usr/bin/env python
# coding: utf-8

# In[1]:


from binance.websockets import BinanceSocketManager
from binance.enums import *
import json

class Fetch_data():
    '''to fetch real-time Candlestick data'''

    global df
    global client

    def fetch_kline(self, symbol, callback, interval):

        bm = BinanceSocketManager(client)

        #start socket
        conn_key = bm.start_kline_socket(symbol, callback, interval)

        return bm



# In[2]:


def process_message(msg):
    ''' the callback function to process fetched real-time data'''

    from datetime import datetime

    global df
    global order_buy

    timestamp = msg['k']['t'] / 1000
    time_star = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

    close = msg['k']['c']
    final = msg['k']['x']

    # store data when this bar is final
    if final == True:
        df = df.append({'close': close, 'datetime': time_star}, ignore_index = True)
        inputs = df['close']
        p = SMA_Strategy(inputs, 3, 10)
        t = p.SmaCross('BTCUSDT')
        print("order buy status: ", order_buy)



# In[3]:


from binance.client import Client
import talib

class SMA_Strategy():

    global client
    global order_buy

    def __init__(self, inputs ,fast, slow):
        self.fast = fast
        self.slow = slow
        self.inputs = inputs

    def cross_up(self, sma_fast, sma_slow):
        if sma_fast.iloc[-1] > sma_slow.iloc[-1] and sma_fast.iloc[-2] <= sma_slow.iloc[-2]:
            return True
        else:
            return False

    def cross_down(self, sma_fast, sma_slow):
        if sma_fast.iloc[-1] < sma_slow.iloc[-1] and sma_fast.iloc[-2] >= sma_slow.iloc[-2]:
            return True
        else:
            return False

    def in_the_market(self):
        if order_buy == {}:
            return True
        else:
            return False

    def SmaCross(self, sym):
        global order_buy

        sma_fast = talib.SMA(self.inputs, timeperiod=self.fast)
        sma_slow = talib.SMA(self.inputs, timeperiod=self.slow)

        if self.cross_up(sma_fast, sma_slow) and not self.in_the_market():
            order_buy = client.create_test_order(symbol=sym, side=Client.SIDE_BUY,                                             type=Client.ORDER_TYPE_MARKET, quantity=100)

        elif self.cross_down(sma_fast, sma_slow) and self.in_the_market():
            # send test sell order
            order_sell = client.create_test_order(symbol=sym, side=Client.SIDE_SELL,                                             type=Client.ORDER_TYPE_MARKET, quantity=100)
            # update order_buy
            order_buy = None



# In[4]:


from binance.client import Client
import pandas as pd
import json

with open('C:/Users/USER/Desktop/binance_api.json', mode='r') as key_file:
    data = json.load(key_file)
    api_key = data['key']
    api_secret = data['secret']

client = Client(api_key, api_secret)

# create a empty dataframe
df = pd.DataFrame(columns=['close', 'datetime'])

# set the original buy position to None(not in the market)
order_buy = None

bm = Fetch_data().fetch_kline(\
            symbol="BTCUSDT", callback=process_message, interval=KLINE_INTERVAL_1MINUTE)


# In[5]:


bm.start()


# In[6]:


bm.close()
