#!/usr/bin/env python
# coding: utf-8

# In[1]:


from data_fetcher2 import BinanceCandle
from strategy_mail2 import SMACross
from broker import Broker
import json


class TradingBot:

    def __init__(self, data, strategy):
        self.data = data
        self.strategy = strategy        

    def run(self):
        self.data.feed(self.strategy.next)


# In[2]:


with open('C:/Users/USER/Desktop/binance_api.json', mode='r') as key_file:
    data_dict = json.load(key_file)
    api_key = data_dict['key']
    api_secret = data_dict['secret']

broker = Broker(api_key, api_secret)
data = BinanceCandle(coin='ETHBTC', freq='1m')
strategy = SMACross(status=0, pfast=10, pslow=30, broker=broker, coin='ETHBTC', quantity=100)
tradingbot = TradingBot(data, strategy)
tradingbot.run()


# In[ ]:




