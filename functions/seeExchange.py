# ---------------------------------------------------------------------------------------------------------------
# Property of Two and Twenty LLP
# ---------------------------------------------------------------------------------------------------------------

# Imported Libraries
import sys
import time
import numpy as np
import datetime as dt
import shift

def seeExchange(trader: shift.Trader, ticker):

    print(ticker, "BID:")
    print("  Price\t\tSize\t  Dest\t\tTime")
    for order in trader.get_order_book_with_destination(ticker, shift.OrderBookType.LOCAL_BID):
        print("%7.2f\t\t%4d\t%6s\t\t%19s" % (order.price, order.size, order.destination, order.time))

    print(" ")

    print(ticker, "ASK:")
    print("  Price\t\tSize\t  Dest\t\tTime")
    for order in trader.get_order_book_with_destination(ticker, shift.OrderBookType.LOCAL_ASK):
        print("%7.2f\t\t%4d\t%6s\t\t%19s" % (order.price, order.size, order.destination, order.time))

    return