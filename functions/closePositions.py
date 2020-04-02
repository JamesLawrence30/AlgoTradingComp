# ---------------------------------------------------------------------------------------------------------------
# Property of Two and Twenty LLP
# ---------------------------------------------------------------------------------------------------------------

# Imported Libraries
import sys
import time
import credentials
import numpy as np
import datetime as dt
import shift

# Imported Functions
from portfolioSummary import portfolioSummary

def closePositions(trader: shift.Trader, ticker, onHand=0, maxAllowed=0):
    """ Takes Trader Object as Input and Closes All Open Orders"""

    if onHand == 0 and maxAllowed == 0:
        # Cancel pending orders
        print("Waiting list size: " + str(trader.get_waiting_list_size()) + " , Canceling all pending orders...")
        for order in trader.get_waiting_list():
            if order.symbol == ticker:
                trader.submit_cancellation(order)
        print("All", ticker, "pending orders cancelled") # Cancel outstanding open orders before entering closing orders

        # Close / Cover all open positions
        #portfolioSummary(trader) # Print summary of portfolio**************************************************************************Good for developing
        item = trader.get_portfolio_item(ticker)
        if item.get_shares() > 0:
            print("Open long positions")
            closeLong = shift.Order(shift.Order.Type.MARKET_SELL, item.get_symbol(), int(item.get_shares() / 100)) # Order size in 100's of shares, strictly as an int
            trader.submit_order(closeLong)
        if item.get_shares() < 0:
            print("Open short positions")
            coverShort = shift.Order(shift.Order.Type.MARKET_BUY, item.get_symbol(), int(item.get_shares() / -100))
            trader.submit_order(coverShort)
        print("All", ticker, "closing orders submitted")


    # Sell one order to regain correct allocation
    else:
        print("Drop one", ticker)
        for order in trader.get_waiting_list():
            if order.symbol == ticker and order.Type == 'Type.LIMIT_SELL': # Cancel an unfilled limit sell so we can replace with market sell
                trader.submit_cancellation(order)
                break # Only cancel one order so that we make sure we have something to sell
        closeLong = shift.Order(shift.Order.Type.MARKET_SELL, ticker, 1) # Sell one to make more bp and reach allocation threshold
        trader.submit_order(closeLong)
    


    return