#!/usr/bin/env python
# coding: utf-8

# ### Task1 Data Fetcher Development
# 1. Websocket data fetcher using Binance

# In[1]:


from binance.client import Client

api_key='FbMo8RNCKlQl2yHsZ8nFWLeT2apXEZPagRZhIs3PoJrePErGQtBgIcGsKfB2q3Ld'
api_secret='YXMWxgfNYy1sJN6ofoA03LgX5aChY8BEeGsar3VxfjdmvN6SOAPrLKZvU0ryXz9o'

client = Client(api_key, api_secret)


# In[3]:


def process_message(msg):
    print("message type: {}".format(msg['e']))
    print(msg)


# In[4]:


from binance.websockets import BinanceSocketManager
from binance.enums import *

bm = BinanceSocketManager(client)

#start socket
conn_key = bm.start_kline_socket('BTCUSDT', process_message)

# then start the socket manager
bm.start()


# In[5]:


bm.close()


# In[ ]:




