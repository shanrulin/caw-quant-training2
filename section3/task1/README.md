# Task1 Data Fetcher Development

In this task, you will learn how to implement data fetcher part of your quant trading system. The difference between the data fetcher in a research framework (like what you wrote in tasks from section1) and the one in a trading system (what you are going to do now) is that the latter requires data flow arriving in a real-time frequency.

In order to achieve this real-time feature, we need to use **Websocket** protocol instead of **REST**. Google these two protocols to see the difference. e.x. [WebSockets vs REST: Understanding the Difference](https://www.pubnub.com/blog/websockets-vs-rest-api-understanding-the-difference/)

## 1. Websocket data fetcher using Binance

take a look at [Binance Python SDK for Websocket endpoint](https://github.com/sammchardy/python-binance/blob/master/binance/websockets.py), write a **script**(.py file), subscribe to **BTC-USDT**'s, **1 minute candle** data. Once you recieve any data, just `print()` it out.

hint:
1. how about class BinanceSocketManager's "start_kline_socket" member function?
2. what's the signature of this function, what's the callback?

## 2. Extract and Transform raw data

the raw data might look like this according to the doc:

```python
{
    "e": "kline",					# event type
    "E": 1499404907056,				# event time
    "s": "ETHBTC",					# symbol
    "k": {
        "t": 1499404860000, 		# start time of this bar
        "T": 1499404919999, 		# end time of this bar
        "s": "ETHBTC",				# symbol
        "i": "1m",					# interval
        "f": 77462,					# first trade id
        "L": 77465,					# last trade id
        "o": "0.10278577",			# open
        "c": "0.10278645",			# close
        "h": "0.10278712",			# high
        "l": "0.10278518",			# low
        "v": "17.47929838",			# volume
        "n": 4,						# number of trades
        "x": false,					# whether this bar is final
        "q": "1.79662878",			# quote volume
        "V": "2.34879839",			# volume of active buy
        "Q": "0.24142166",			# quote volume of active buy
        "B": "13279784.01349473"	# can be ignored
        }
}
```

However, we can't use it directly in our trading system. Everything needs to be formatted in a good way and some need to be discarded. Why not format it like the way as we did for backtrader. 

|close|high|low|open|volume|baseVolume|datetime|
|-----|----|---|----|------|----------|--------|
|4094.62|4124.69|4094.62|4124.69|0.3476|1428.52|2017-08-20 03:01:00|
|4093.0|4094.62|4091.8|4094.62|0.8092|3313.4|2017-08-20 03:02:00|
|4117.41|4142.16|4087.0|4093.0|10.74|44122.84|2017-08-20 03:03:00|

Note: this is a table representation of pd.Dataframe. Each raw data is one record (one row). Now, instead of just printing the data by `print()`, every time you recieve new data, you should format the data and append it to the end of this pd.Dataframe by passing a new function as callback that does this, so that you get a full history of kline data.

## 3. Output the kline flow

In some cases, you would want to save this candle data to your database for recording or further analysis. However, choosing a local database like mysql, postgresql or cloud database like AWS's RDS or Dynamodb, configuring it, and writing to it is way beyond the scope of this training program. To simply the question, we just save it to a csv file.

Find a way to just write a new line(instead of overwriting it completely) to the csv once you recieve and format the data. 

In the end, you should see your csv file growing by one row every minute.




