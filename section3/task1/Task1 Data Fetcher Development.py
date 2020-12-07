#!/usr/bin/env python
# coding: utf-8

# ### Task1 Data Fetcher Development
# 2. Extract and Transform raw data
# 3. Output the kline flow

# In[1]:


from binance.client import Client
import pandas as pd

api_key='FbMo8RNCKlQl2yHsZ8nFWLeT2apXEZPagRZhIs3PoJrePErGQtBgIcGsKfB2q3Ld'
api_secret='YXMWxgfNYy1sJN6ofoA03LgX5aChY8BEeGsar3VxfjdmvN6SOAPrLKZvU0ryXz9o'

client = Client(api_key, api_secret)

# create a empty dataframe 
df = pd.DataFrame(columns=['close', 'high', 'low', 'open', 'volume', 'baseVolume', 'datetime'])


# In[2]:


def process_message(msg):
    from datetime import datetime
    import pandas as pd
    
    global df
    
    timestamp=msg['k']['t']/1000
    time_star=datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
   
    close=msg['k']['c']
    high=msg['k']['h']
    low=msg['k']['l']
    open_p=msg['k']['o']
    volume=msg['k']['v']
    baseVolume=msg['k']['q']
    final=msg['k']['x']
    
    # store data when this bar is final
    if final==True:
        df= df.append({'close': close, 'high': high, 'low': low, 'open' : open_p,                         'volume': volume, 'baseVolume': baseVolume, 'datetime': time_star}, ignore_index = True)
        last_idx=str(df.index[-1])
        #print(df)
        df.to_csv ('candle_data_'+last_idx+'.csv', index = False, header=True)
    


# In[3]:


from binance.websockets import BinanceSocketManager
from binance.enums import *

bm = BinanceSocketManager(client)

#start socket
conn_key = bm.start_kline_socket('BTCUSDT', process_message,interval=KLINE_INTERVAL_1MINUTE)

# then start the socket manager
bm.start()


# In[4]:


bm.close()


# In[5]:


#df


# In[ ]:




