# Task2 Strategy Development

During the last task, you learned how to maintain a data stream(information flow) in your trading system. As a event-driven trading framwork, now it's time to use the data to create some trading signals and make investment decision based on that.

## 1. TA-Lib

[TA-Lib](https://ta-lib.org/) is a toolbox written in C, widely used by trading software developers requiring to perform **technical analysis** of financial market data.

1. [install TA-Lib](https://mrjbq7.github.io/ta-lib/install.html) for your  specific OS
2. Check its [Doc](https://mrjbq7.github.io/ta-lib/doc_index.html) and figure out what it is, how to use it and then play with it.(You may use your data in section1/task1 to calculate some technical indicators)
3. Instead of outputing a csv file in task1, feed task1's **real-time updating** candle data in TA-Lib to compute indicators. So instead of adding one line every iteration, now you should see new indicator values every iteration.

## 2. Trading signal

We will use SMACross again to manifest the idea. Now use TA-Lib to:

1. Compute 2 techinical indicators: **SMA fast** and **SMA slow**
2. Generate buy signal if SMA fast **cross up** SMA slow, sell signal if SMA fast **cross down** SMA slow.
3. Create a market buy order if buy signal occurs and not in the market. On the contrary, liquid out if sell signal occurs and in the market.
4. Print useful information when there's some action taking place.

Note:

1. You only need part of your real-time updated candle data. In this case, `candle['close']` to compute SMA.
2. By saying "generate buy/sell signals", I mean to write some functions like below. Then basing on True or False, you can decide whether to buy or sell.

```python
def cross_up(sma_fast, sma_slow):
    if something:
        return True
    else:
        return False
```

3. You can just create a test order like what you did in section1/task2. In real world, you may create market order, limit order, stop loss order, stop trail order and etc according to your trading strategy.

```python
if cross_up and not in_the_market:
    create_market_buy()
elif cross_down and in_the_market:
    create_market_sell()
```

4. To determine whether we are in the market or not, you may record this information in some variable like `self.position` like backtrader.

5. To make it quicker to debug and test, you may use higher frequency data like 1min candle.

## 3. Modularize your code

Notice that data fecther does nothing to do with trading strategy and vice verse. Ensure that it's so in your code by separating data fecther from trading strategy.

Consider:

1. define **modules** by their different functionalities, in this case, data fetcher and trading strategy.
2. write unrelated stuffs(modules) in different functions, classes, files or even folders.
3. your code should be flexible to switch between trading assets(e.x. BTC-USDT to ETH-USDT), frequencies(e.x. 1min to 1hour), strategies(e.x. SMACross to others) and strategy parameters(e.x. sma5 to sma10)