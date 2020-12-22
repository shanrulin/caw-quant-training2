from binance.websockets import BinanceSocketManager
from binance.client import Client
import json


class BinanceCandle:
    
    def __init__(self, coin='ETHBTC', freq='1m'):
        
        self.coin = coin
        self.freq = freq

        with open('C:/Users/USER/Desktop/binance_api.json', mode='r') as key_file:
            self.data_dict = json.load(key_file)
            self.api_key = self.data_dict['key']
            self.api_secret = self.data_dict['secret']

        self.client = Client(self.api_key, self.api_secret)
        self.bm = BinanceSocketManager(self.client)

    def feed(self, callback):
        self.bm.start_kline_socket(self.coin, callback, self.freq)
        self.bm.start()

    