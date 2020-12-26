from binance.client import Client
from binance.enums import *
import json


class Broker:

    def __init__(self, api_file_path='C:/Users/USER/Desktop/binance_api.json', coin='ETHBTC'):
        with open(api_file_path, mode='r') as key_file:
            self.api_data = json.load(key_file)
            self.api_key = self.api_data['key']
            self.api_secret = self.api_data['secret']

        self.client = Client(self.api_key, self.api_secret)
        self.coin = coin

    def buy(self):
        test_buy = self.client.create_test_order(symbol=self.coin, side=self.client.SIDE_BUY,\
            type=self.client.ORDER_TYPE_MARKET, quantity=100)

    def sell(self):
        test_sell = self.client.create_test_order(symbol=self.coin, side=self.client.SIDE_SELL,\
            type=self.client.ORDER_TYPE_MARKET, quantity=100)
