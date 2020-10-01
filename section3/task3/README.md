# Task3 Logging and Notification

During the last task, you learned how to use data and logic to generate trading signal, based on which you buy or sell. However, you need to know more in details about how your system is working by developing some logging and notification module.

## 1. Logging

[logging](https://docs.python.org/3/library/logging.html#) is a built-in python module that could meet your logging needs easily. Take a look at its Doc. e.x. [Basic Logging Tutorial](https://docs.python.org/3/howto/logging.html#basic-logging-tutorial), [Logging Cookbook](https://docs.python.org/3/howto/logging-cookbook.html#logging-cookbook), or even [Advanced Tutorial](https://docs.python.org/3/howto/logging.html#logging-advanced-tutorial). Read the tutorial, try the examples, and think about what features/functionality it gives over `print()` and how you could use it in your trading system.

Milestones:

1. You should be able to seperate different log messages by **Level** according to their importance. For example, **DEBUG** for operational logs (e.x. Trading system initialization, Data loading, program flow message and etc) **INFO** for computed indicators' values(most recent sma5 value), position status, trading opertaion and etc.
2. You should be able to use [Handler](https://docs.python.org/3/howto/logging.html#handlers). E.x. Log everything to STDOUT by [StreamHandler](https://docs.python.org/3/library/logging.handlers.html#streamhandler) and log more important information like trading operations to a `.log` file by [FileHandler](https://docs.python.org/3/library/logging.handlers.html#filehandler).
3. You should also use [Formatter](https://docs.python.org/3/library/logging.html#logging.Formatter) based on your prefered formatting style. E.x. "2020-09-30 21:21:29,294 INFO main() - Trade initiating...[BTC-USDT]"

## 2. Telegram and Email notification

Normally your trading system should be running 24/7 on a cloud server. It's impossible to monitor it all the time. Thus, you might need further notification functionality which notifies you important behaviors of your trading system (like buying/selling an asset), and also, error messages if it somewhat breaks down.

Assume for normal notification, you want to have a telegram bot; for errors, you want to get notified by an email.

### Telegram notification bot

- [python-telegram-bot Github Repo](https://github.com/python-telegram-bot/python-telegram-bot)
- [python-telegram-bot Doc](https://python-telegram-bot.readthedocs.io/en/stable/)
- [python-telegram-bot examples](https://github.com/python-telegram-bot/python-telegram-bot/tree/master/examples)

Make sure you get a telegram app installed on you IOS/Andriod phone(prefered), or PC. Then you need to create a telegram bot from **BotFather**, check out [here](https://core.telegram.org/bots#3-how-do-i-create-a-bot). After you get bot's **Token**, you need to add your bot as contact and **start** the bot. Then you can use **python-telegram-bot** library to control the bot and send message to yourself.

Use telegram bot to send yourself a message if there's any trade happening. In the message, information like trading direction, order type, volume and etc might be included so you know what's exactly happening.

### Email notification

I've written a blog talking about how to send email using python, there's an example using gmail to send yourself emails. Check out [here](https://xyshell.github.io/2020/09/05/email-note/).  There are also other helpful blogs to take a look at if you want to use other vendors like QQ mail for example. 

In this case, if your program crashed and quited, you might send yourself a email. Think about how to do this by Error Handling.

- [Sending Emails in Python — Tutorial with Code Examples](https://julien.danjou.info/sending-emails-in-python-tutorial-code-examples/)
- [简单三步，用 Python 发邮件](https://zhuanlan.zhihu.com/p/24180606)
