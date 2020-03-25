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
from closePositions import closePositions

def firstStrategy(trader: shift.Trader, ticker, dayEnd, lag, fillTime, adjustment):
    fillTime=fillTime*10

    # Datetime of simulation
    rightNow =  trader.get_last_trade_time()

    # FIFO queue initialized
    priceQueue = []

    signal = 'S' # Force to start with long position
    count = 1
    # While the time is before end of day...
    while(dayEnd > rightNow):
        # Pause and wait for change in prices
        time.sleep(lag)
        print(rightNow, "Total P/L:",trader.get_portfolio_summary().get_total_realized_pl())
        """
        Make Trades Here:
        """
        if count % (lag*50) == 0 or trader.get_portfolio_summary().get_total_bp() < 150000: # Every so often, sell off inventory.  Wait longer if lower lag ((1/lag)*15)
            closePositions(trader) # Free up buying power and reduce risk
            signal = 'S' # Force to start with long position
            print("Sold inventory, risk & bp reset")

        if len(priceQueue) > 2: # Queue is full
            firstDeriv = np.gradient(priceQueue, 1) # Find rate of change of prices
            print("deriv =", firstDeriv[2])

            # Prices switch from decreasing to increasing = buy  [buy @ local minima]
            if firstDeriv[2] > 0 and signal is 'S':
                buySize = max(1,round(trader.get_best_price(ticker).get_ask_size() / 3)) # Only buy as much as you can sell. Divide by __ so buying power lasts on high volume. At least 1
                buyPrice = (trader.get_best_price(ticker).get_bid_price() +  trader.get_best_price(ticker).get_ask_price())/2 # Buy at Mid Price
                limit_buy = shift.Order(shift.Order.Type.LIMIT_BUY, ticker, buySize, buyPrice-adjustment)
                trader.submit_order(limit_buy)
                print("Buy", buySize, "@", buyPrice)

                # Give the order time to fill
                waitCount = 1
                while trader.get_order(limit_buy.id).status != shift.Order.Status.FILLED and waitCount <= fillTime and trader.get_order(limit_buy.id).status != shift.Order.Status.REJECTED:
                    print(waitCount, "Status:",trader.get_order(limit_buy.id).status)
                    time.sleep(.1)
                    waitCount = waitCount + 1
                print(waitCount, trader.get_order(limit_buy.id).status)

                if trader.get_order(limit_buy.id).status == shift.Order.Status.REJECTED:
                    print("Rejected")

                elif trader.get_order(limit_buy.id).status == shift.Order.Status.NEW or trader.get_order(limit_buy.id).status == shift.Order.Status.PENDING_NEW:
                    trader.submit_cancellation(limit_buy)
                    print("Cancelled")

                else: # trader.get_order(limit_buy.id).status == shift.Order.Status.PARTIALLY_FILLED or trader.get_order(limit_buy.id).status == shift.Order.Status.FILLED:
                    signal = 'B'
                    print("Buy registered")

            # Prices switch from increasing to decreasing = sell  [sell @ local maxima]
            sellPrice = (trader.get_best_price(ticker).get_bid_price() +  trader.get_best_price(ticker).get_ask_price())/2 # Sell at Mid Price
            if firstDeriv[2] < 0 and signal is 'B' and sellPrice > trader.get_portfolio_item(ticker).get_price(): # Only sell for a profit, don't accept a loss here
                sellSize = min(trader.get_portfolio_item(ticker).get_shares(),trader.get_best_price(ticker).get_bid_size()) # Sell as much as market asks for, or all we have - whichever is less
                limit_buy = shift.Order(shift.Order.Type.LIMIT_SELL, ticker, sellSize, sellPrice+adjustment)
                trader.submit_order(limit_buy)
                print("Sell", sellSize, "@", sellPrice)

                # Give the order time to fill
                waitCount = 1
                while trader.get_order(limit_buy.id).status != shift.Order.Status.FILLED and waitCount <= fillTime and trader.get_order(limit_buy.id).status != shift.Order.Status.REJECTED:
                    print(waitCount, "Status:",trader.get_order(limit_buy.id).status)
                    time.sleep(.1)
                    waitCount = waitCount + 1
                print(waitCount, trader.get_order(limit_buy.id).status)

                if trader.get_order(limit_buy.id).status == shift.Order.Status.REJECTED:
                    print("Rejected")
                    if sellSize == 0:
                        signal = 'S' # Not holding any shares..reset last trade so we can begin to buy

                elif trader.get_order(limit_buy.id).status == shift.Order.Status.NEW:
                    trader.submit_cancellation(limit_buy)
                    print("Cancelled")

                else: # trader.get_order(limit_buy.id).status == shift.Order.Status.PARTIALLY_FILLED or trader.get_order(limit_buy.id).status == shift.Order.Status.FILLED:
                    signal = 'S'
                    print("Sell registered")
                    count = count - 2 # lower count

            elif firstDeriv[2] < 0 and signal is 'B' and sellPrice <= trader.get_portfolio_item(ticker).get_price(): # Could not sell for a profit, but attempted to sell
                signal = 'S'
                print("Inventory held")

            # Drop oldest price, shift the prices over, add the newest price to queue
            priceQueue[0]=priceQueue[1]
            priceQueue[1]=priceQueue[2]
            priceQueue[2]=(trader.get_best_price(ticker).get_bid_price() +  trader.get_best_price(ticker).get_ask_price())/2 # Mid Price

        else: # Queue is not full
            priceQueue.append((trader.get_best_price(ticker).get_bid_price() +  trader.get_best_price(ticker).get_ask_price())/2) # Fill the queue from oldest price to latest price, using Mid Price


        rightNow =  trader.get_last_trade_time() # Reset datetime of right now
        count = count + 1

    # 90 seconds till end of trading day
    closePositions(trader)

    # Done trading
    return