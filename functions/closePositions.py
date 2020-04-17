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

def closePositions(trader: shift.Trader, ticker):

    # Cancel pending orders
    print("Waiting list size:", trader.get_waiting_list_size())
    for order in trader.get_waiting_list():
        if order.symbol == ticker:
            trader.submit_cancellation(order)
    print("All", ticker, "pending orders cancelled") # Cancel open orders before submitting closing orders

    # Close / Cover all open positions
    #portfolioSummary(trader) # Print summary of portfolio**************************************************************************Good for developing
    item = trader.get_portfolio_item(ticker)
    if item.get_shares() > 0:
        closeLong = shift.Order(shift.Order.Type.MARKET_SELL, item.get_symbol(), int(item.get_shares() / 100)) # Order size in 100's of shares, strictly as an int
        trader.submit_order(closeLong)
        #print("Close all long positions")
    elif item.get_shares() < 0:
        coverShort = shift.Order(shift.Order.Type.MARKET_BUY, item.get_symbol(), int(item.get_shares() / -100))
        trader.submit_order(coverShort)
        #print("Close all short positions")
    print("All", ticker, "closing orders submitted")

    return