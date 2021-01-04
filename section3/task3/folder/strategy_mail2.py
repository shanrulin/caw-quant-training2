import talib
import pandas as pd
from broker import Broker
from mylogger import logger, telegram_msg


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
        self.logger = logger()
        
        self.logger.debug("trading setting: coin {}, quantity {}".format(self.coin, self.qty))
        self.logger.debug('initial postiion status = {}'.format(self.status))

    def next(self, candle):
        #print(candle)

        close = candle['k']['c']
        final = candle['k']['x']
        self.logger.debug("Load candle data")

        if final == True:
            self.df = self.df.append({'close': close}, ignore_index = True)
            #print(self.df.values[-1])
            inputs = self.df['close']
            fast = talib.SMA(inputs, timeperiod=self.pfast)
            slow = talib.SMA(inputs, timeperiod=self.pslow)
            self.logger.info("SMA fast is {}, SMA slow is {}".format(fast.iloc[-1], slow.iloc[-1]))

            if cross_up(fast, slow).iloc[-1] and self.status == 0:

                try:
                    self.logger.info("Go into market signal")
                    ## send buy order
                    test_order = self.broker.buy(coin=self.coin, quantity=self.qty)
                    self.logger.info("Buy order {}".format(test_order))

                    # send message to telegram
                    message = 'Go into market signal: Buy {} with quantity {} at market price'.format(self.coin, self.qty)
                    telegram_msg(message=message)

                    ## update self.status
                    self.status = 1
                    self.logger.info("position status is {}".format(self.status))

                except:
                    # send error to email
                    self.logger.error('ERROR in buying')

            elif cross_down(fast, slow).iloc[-1] and self.status == 1:
                try:
                    self.logger.info("Exit market signal")
                    ## send sell order
                    sell_order = self.broker.sell(coin=self.coin, quantity=self.qty)
                    self.logger.info("Sell order {}".format(sell_order))

                    # send message to telegram
                    message = 'Exit market signal: Sell {} with quantity {} at market price'.format(self.coin, self.qty)
                    telegram_msg(message=message)

                    ## update self.status
                    self.status = 0
                    self.logger.info("position status is {}".format(self.status))

                except:
                    # send error to email
                    self.logger.error('ERROR in selling')

