from binance.client import Client
from binance.enums import *


class Broker:

    def __init__(self, api_key, api_secret):
        self.client = Client(api_key, api_secret)

    def buy(self, coin, quantity):
        test_buy = self.client.create_test_order(symbol=coin, side=self.client.SIDE_BUY,\
            type=self.client.ORDER_TYPE_MARKET, quantity=quantity)
        return test_buy

    def sell(self, coin, quantity):
        test_sell = self.client.create_test_order(symbol=coin, side=self.client.SIDE_SELL,\
            type=self.client.ORDER_TYPE_MARKET, quantity=quantity)
        return test_sell
