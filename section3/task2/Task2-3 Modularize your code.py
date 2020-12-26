from data_fetcher2 import BinanceCandle
from strategy2 import SMACross


class TradingBot:

    def __init__(self, data, strategy):
        self.data = data
        self.strategy = strategy        

    def run(self):
        self.data.feed(self.strategy.next)

if __name__ == "__main__":
    data = BinanceCandle(coin='ETHBTC', freq='1m')
    strategy = SMACross(status=0, pfast=10, pslow=30)
    tradingbot = TradingBot(data, strategy)
    tradingbot.run()
