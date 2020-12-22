import talib
import pandas as pd



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

def buy(client_param):
    ''' buy order '''
    buy_order = client_param.client.create_test_order(symbol=client_param.coin, side=client_param.client.SIDE_BUY,\
        type=client_param.client.ORDER_TYPE_MARKET, quantity=100)
    #print("buy order", buy_order)

def sell(client_param):
    ''' sell order'''
    sell_order = client_param.client.create_test_order(symbol=client_param.coin, side=client_param.client.SIDE_SELL,\
        type=client_param.client.ORDER_TYPE_MARKET, quantity=100)
    #print("sell order", sell_order)


class SMACross:

    def __init__(self, status, pfast, pslow, outer): 
        self.status = status # status = 0 means not in the market
        self.pfast = pfast
        self.pslow = pslow
        self.df = pd.DataFrame(columns=['close'])
        self.outer = outer  

    def next(self, candle):
        #print(candle)
        
        close = candle['k']['c']
        final = candle['k']['x']
        
        if final == True:
            self.df = self.df.append({'close': close}, ignore_index = True)
            print(self.df)
            inputs = self.df['close']
            fast = talib.SMA(inputs, timeperiod=self.pfast)
            slow = talib.SMA(inputs, timeperiod=self.pslow)

            if cross_up(fast, slow).iloc[-1] and self.status == 0: 
                #print("Go into market signal")
                ## send buy order
                buy(self.outer) 
                ## update self.status
                self.status = 1

            elif cross_down(fast, slow).iloc[-1] and self.status == 1:
                #print("Exit market signal")
                ## send sell order
                sell(self.outer)
                ## update self.status
                self.status = 0



        



