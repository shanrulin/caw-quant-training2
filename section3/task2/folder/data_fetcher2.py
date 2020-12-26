from binance.websockets import BinanceSocketManager
from binance.client import Client



class BinanceCandle:
    
    def __init__(self, coin='ETHBTC', freq='1m'):
        
        self.coin = coin
        self.freq = freq
        self.client = Client("", "")
        self.bm = BinanceSocketManager(self.client)

    def feed(self, callback):
        self.bm.start_kline_socket(self.coin, callback, self.freq)
        self.bm.start()

    