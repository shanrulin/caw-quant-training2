#!/usr/bin/env python
# coding: utf-8

# In[1]:


from binance.client import Client
import pandas as pd

with open('C:/Users/USER/Desktop/binance_api.json', mode='r') as key_file:
    data = json.load(key_file)
    api_key = data['key']
    api_secret = data['secret']

client = Client(api_key, api_secret)

# create a empty dataframe
df = pd.DataFrame(columns=['close', 'high', 'low', 'open', 'volume', 'baseVolume', 'datetime'])


# In[4]:


def process_message(msg):
    from datetime import datetime
    import pandas as pd
    import talib

    global df

    timestamp = msg['k']['t'] / 1000
    time_star = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

    close = msg['k']['c']
    high = msg['k']['h']
    low = msg['k']['l']
    open_p = msg['k']['o']
    volume = msg['k']['v']
    baseVolume = msg['k']['q']
    final = msg['k']['x']

    # store data when this bar is final
    if final == True:
        df = df.append({'close': close, 'high': high, 'low': low, 'open' : open_p, \
        'volume': volume, 'baseVolume': baseVolume, 'datetime': time_star}, ignore_index = True)
        inputs = df['close']
        output = talib.SMA(inputs, timeperiod=5)
        print(output)



# In[5]:


from binance.websockets import BinanceSocketManager
from binance.enums import *

bm = BinanceSocketManager(client)

#start socket
conn_key = bm.start_kline_socket('BTCUSDT', process_message,interval=KLINE_INTERVAL_1MINUTE)

# then start the socket manager
bm.start()


# In[6]:


bm.close()
