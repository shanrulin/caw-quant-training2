#!/usr/bin/env python
# coding: utf-8

# In[1]:


from binance.client import Client
import pandas as pd
import json

with open('C:/Users/USER/Desktop/binance_api.json', mode='r') as key_file:
    data = json.load(key_file)
    api_key = data['key']
    api_secret = data['secret']

client = Client(api_key, api_secret)

# create an empty dataframe 
df = pd.DataFrame(columns=['close', 'datetime'])

# set the original buy position to None(not in the market)
order_buy = None


# In[2]:


def cross_up(sma_fast, sma_slow):
    if sma_fast.iloc[-1] > sma_slow.iloc[-1] and sma_fast.iloc[-2] <= sma_slow.iloc[-2]:
        return True
    else:
        return False


# In[3]:


def cross_down(sma_fast, sma_slow):
    if sma_fast.iloc[-1] < sma_slow.iloc[-1] and sma_fast.iloc[-2] >= sma_slow.iloc[-2]:
        return True
    else:
        return False


# In[4]:


def in_the_market(order_buy):
    if order_buy == {}: 
        return True
    else: 
        return False 


# In[5]:


def process_message(msg):
    ''' a callback function to process real-time data'''
    
    from datetime import datetime
    import pandas as pd
    import numpy as np
    import talib
    
    global df
    global order_buy
    global sma_fast
    global sma_slow
    
    timestamp = msg['k']['t'] / 1000
    time_star = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
   
    close = msg['k']['c']
    final = msg['k']['x']
    
    # store data when this bar is final
    if final == True:
        df = df.append({'close': close, 'datetime': time_star}, ignore_index = True)
        inputs = df['close']
        sma_fast = talib.SMA(inputs, timeperiod=5)
        sma_slow = talib.SMA(inputs, timeperiod=10)    
        
        if cross_up(sma_fast, sma_slow) and not in_the_market(order_buy):            
            order_buy = client.create_test_order(symbol='BTCUSDT', side=Client.SIDE_BUY,                                             type=Client.ORDER_TYPE_MARKET, quantity=100)
           
        elif cross_down(sma_fast, sma_slow) and in_the_market(order_buy):
            # send test sell order
            order_sell = client.create_test_order(symbol='BTCUSDT', side=Client.SIDE_SELL,                                             type=Client.ORDER_TYPE_MARKET, quantity=100)
            # update order_buy
            order_buy = None    


# In[6]:


from binance.websockets import BinanceSocketManager
from binance.enums import *

bm = BinanceSocketManager(client)

#start socket
conn_key = bm.start_kline_socket('BTCUSDT', process_message,interval=KLINE_INTERVAL_1MINUTE)

# then start the socket manager
bm.start()


# In[7]:


bm.close()

