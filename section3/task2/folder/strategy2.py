import talib
import pandas as pd
from broker import Broker



def cross_up(fast: pd.Series, slow: pd.Series) -> pd.Series:
    '''Compute cross up indicator
    '''
    blw = fast.shift(1) < slow.shift(1)
    upn = fast > slow
    return upn & blw


def cross_down(fast: pd.Series, slow: pd.Series) -> pd.Series:
    '''Compute cross down indicator
    '''
    upn = fast.shift(1) > slow.shift(1)
    blw = fast < slow
    return upn & blw


class SMACross:

    def __init__(self, status, pfast, pslow, broker, coin, quantity):
        self.status = status # status = 0 means not in the market
        self.pfast = pfast
        self.pslow = pslow
        self.df = pd.DataFrame(columns=['close'])
        self.coin = coin
        self.qty = quantity
        self.broker = broker

    def next(self, candle):
        #print(candle)

        close = candle['k']['c']
        final = candle['k']['x']

        if final == True:
            self.df = self.df.append({'close': close}, ignore_index = True)
            #print(self.df.values[-1])
            inputs = self.df['close']
            fast = talib.SMA(inputs, timeperiod=self.pfast)
            slow = talib.SMA(inputs, timeperiod=self.pslow)

            if cross_up(fast, slow).iloc[-1] and self.status == 0:
                #print("Go into market signal")
                ## send buy order
                self.broker.buy(coin=self.coin, quantity=self.qty)
                ## update self.status
                self.status = 1

            elif cross_down(fast, slow).iloc[-1] and self.status == 1:
                #print("Exit market signal")
                ## send sell order
                self.broker.sell(coin=self.coin, quantity=self.qty)
                ## update self.status
                self.status = 0
