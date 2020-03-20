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

def marketMaker(trader: shift.Trader, ticker, dayEnd, lag):

    # Datetime of simulation
    rightNow =  trader.get_last_trade_time()

    count = 1
    # While the time is before end of day...
    while(dayEnd > rightNow):
        print(rightNow, "Total P/L:",trader.get_portfolio_summary().get_total_realized_pl())
        """
        Make Trades Here:
        """
        if count % ((1/lag)*10) == 0: # Every so often, sell off inventory.  Wait longer if lower lag
        	closePositions(trader)
        	print("Sold inventory, risk reset")

        time.sleep(lag) # Give prices some time to change

        # Submit a buy order
        limit_buy = shift.Order(shift.Order.Type.LIMIT_BUY, ticker, 1, trader.get_best_price(ticker).get_bid_price()) # Can buy +0.5 above bid with wide spread, or -.01 below if high volume
        trader.submit_order(limit_buy)
        print("Bought")

        time.sleep(0.1) # Allow a brief time for the order to fill

        # Sell if the buy order filled
        if trader.get_order(limit_buy.id).status == shift.Order.Status.FILLED:
        	limit_sell = shift.Order(shift.Order.Type.LIMIT_SELL, ticker, 1, trader.get_best_price(ticker).get_ask_price()) # Can sell -.05 below ask with wide spread, or +.01 above if high volume
        	trader.submit_order(limit_sell)
        	print("Filled buy and Sold")

        # Otherwise cancel the buy order
        else:
            for order in trader.get_waiting_list():
                trader.submit_cancellation(order)
            print("Cancelled")

        count = count + 1 # Increment counter
        rightNow =  trader.get_last_trade_time() # Reset datetime of right now

    # 60 seconds till end of trading day
    closePositions(trader)

    # Done trading
    return