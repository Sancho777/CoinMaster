import praw
import config
from textblob import TextBlob
from binance.client import Client
from binance.enums import *


client = Client(config.BYNANCE_KEY, config.BYNANCE_SECRET)
info = client.get_account()
# print(info)

reddit = praw.Reddit(
    client_id=config.REDDIT_ID,
    client_secret=config.REDDIT_SECRET,
    password=config.REDDIT_PASS,
    user_agent="sentimentanalysisbots",
    username=config.REDDIT_USER,
)

sentimentList = []
neededSentiments = 300

TRADE_SYMBOL = 'BTCUSDT'
TRADE_QUANTITY = 0.0001
in_position = False


def Average(lst):
    if len(lst) == 0:
        return len(lst)
    else:
        return sum(lst[-neededSentiments:])/neededSentiments


def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        print('sending order')
        order = client.create_order(
            symbol=symbol, side=side, type=order_type, quantity=quantity)
        print(order)
    except Exception as e:
        print('An exception has ocurred ' + e)
        return False
    return True


for comment in reddit.subreddit("bitcoinmarkets").stream.comments():
    print(comment.body)

    redditComment = comment.body
    blob = TextBlob(redditComment)

    # print(blob.sentiment)

    sent = blob.sentiment
    print(" *************** Sentiment is:  " + str(sent.polarity))

    if sent.polarity != 0.0:
        sentimentList.append(sent)

        # print(" *************** TOTAL SENTIMENT OF LIST IS:  " +
        #       str(round(Average(sentimentList))))

        if len(sentimentList) > neededSentiments and round(Average(sentimentList)) > 0.5:
            print("BUY: " + str(Average(sentimentList)))
            if in_position:
                print(" *************** BUY ORDER BUT WE OWN *************** ")
            else:
                print(" *************** BUY ORDER *************** ")
                order_succeeded = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
                if order_succeeded:
                    in_position = True
        elif len(sentimentList) > neededSentiments and round(Average(sentimentList)) < -0.5:
            print("SELL: " + str(Average(sentimentList)))
            if in_position:
                order_succeeded = order(
                    SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
                if order_succeeded:
                    in_position = False
            else:
                print(" *************** SELL ORDER BUT WE DON'T OWN *************** ")
