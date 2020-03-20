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

def firstStrategy(trader: shift.Trader, ticker, dayEnd, lag):

    # Datetime of simulation
    rightNow =  trader.get_last_trade_time()

    # FIFO queue initialized
    priceQueue = []

    signal = 'S'
    # While the time is before end of day...
    while(dayEnd > rightNow):
        # Pause and wait for change in prices
        time.sleep(lag)
        print(rightNow, "Total P/L:",trader.get_portfolio_summary().get_total_realized_pl())
        """
        Make Trades Here:
        """
        if len(priceQueue) > 2: # Queue is full
            firstDeriv = np.gradient(priceQueue, 1) # Find rate of change of prices

            # Prices switch from decreasing to increasing = buy  [buy @ local minima]
            if firstDeriv[2] > 0 and signal is 'S':
                #trader.cancel_all_pending_orders() # Make sure we have buying power
                limit_buy = shift.Order(shift.Order.Type.LIMIT_BUY, ticker, 10, trader.get_best_price(ticker).get_bid_price())
                trader.submit_order(limit_buy)
                print("buy @", trader.get_last_price(ticker))
                signal = 'B'
            # Prices switch from increasing to decreasing = sell  [sell @ local maxima]
            elif firstDeriv[2] < 0 and signal is 'B':
                #trader.cancel_all_pending_orders() # Make sure we have buying power
                limit_buy = shift.Order(shift.Order.Type.LIMIT_SELL, ticker, 10, trader.get_best_price(ticker).get_ask_price())
                trader.submit_order(limit_buy)
                print("sell @", trader.get_last_price(ticker))
                signal = 'S'

            # Drop oldest price, shift the prices over, add the newest price to queue
            priceQueue[0]=priceQueue[1]
            priceQueue[1]=priceQueue[2]
            priceQueue[2]=trader.get_last_price(ticker)

        else: # Queue is not full
            priceQueue.append(trader.get_last_price(ticker)) # Fill the queue from oldest price to latest price


        rightNow =  trader.get_last_trade_time() # Reset datetime of right now

    # 90 seconds till end of trading day
    closePositions(trader)

    # Done trading
    return