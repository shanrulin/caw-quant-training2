import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

gmail = os.environ.get('GMAIL_USER')
mail_pass = os.environ.get('GMAIL_PASS')

token = os.environ.get('TELE_TOKEN')
chat_id = os.environ.get('TELE_CHAT_ID')

def logger():
    ''' a logging function shows operational logs on console,
    saves trading logs to file and sends error logs to email'''

    # create logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # create file handler which logs even debug message
    fh = logging.FileHandler('trading_log.log')
    fh.setLevel(logging.INFO)

    # create console handler and set level to debug
    ch = logging.StreamHandler() 
    ch.setLevel(logging.DEBUG)

    # create mail handler 
    mh = logging.handlers.SMTPHandler(mailhost=('smtp.gmail.com', 587), fromaddr=gmail, \
        toaddrs=[gmail],subject='ERROR Log Mail', credentials=(gmail,mail_pass), secure=())
    mh.setLevel(logging.ERROR)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    mh.setFormatter(formatter)


    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    logger.addHandler(mh)

    return logger


def telegram_msg(message, token=token, chat_id=chat_id):
    ''' a function sends log to telegram'''

    updator = Updater(token, use_context=True)
    telegram_msg = updator.bot.send_message(chat_id, message)
    
    return telegram_msg
    