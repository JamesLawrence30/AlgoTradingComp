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

def marketMaker(trader: shift.Trader, ticker, dayEnd, allocation, orderType, lag=3, fillTime=30, spreadWiden=0.00):

    # Datetime of simulation
    rightNow =  trader.get_last_trade_time()

    fillTime = fillTime*10
    # While the time is before end of day...
    while dayEnd > rightNow:
        time.sleep(lag) # Give prices some time to change
        """
        Make Trades Here:
        """
        onHand = trader.get_portfolio_item(ticker).get_shares()*((trader.get_best_price(ticker).get_bid_price()+trader.get_best_price(ticker).get_ask_price())/2) # Portfolio value of the stock
        maxAllowed = allocation*(1000000 + trader.get_portfolio_summary().get_total_realized_pl()) # Maximum portfolio allocation for this stock
        print(ticker, "on hand:", round(onHand,2), "max:", round(maxAllowed), "    P/L:", round(trader.get_portfolio_summary().get_total_realized_pl(),2), " Waiting list:", trader.get_waiting_list_size())
        
        if onHand > maxAllowed and orderType == shift.Order.Type.LIMIT_BUY: # Holding too much
        	continue # Allow Sell side to catch up
        elif onHand < -maxAllowed and orderType == shift.Order.Type.LIMIT_SELL: # Short too much
        	continue # Allow Buy side to catch up

        time.sleep(lag) # Give prices some time to change

        # Submit an order
        bid = trader.get_best_price(ticker).get_bid_price()
        ask = trader.get_best_price(ticker).get_ask_price()
        spreadWiden = max(.01, (ask-bid)*.25)
        if (ask-bid) < .05: # If spread is too tight, widen it
        	spreadWiden = -spreadWiden

        if orderType == shift.Order.Type.LIMIT_BUY:
        	size = max(1,round(trader.get_best_price(ticker).get_ask_size() / 5)) # Only buy as much as you can sell. Divide by 5 so buying power lasts on high volume. At least 1
        	price = bid+spreadWiden # Can buy above bid if wide spread, or below bid if high volume
        elif orderType == shift.Order.Type.LIMIT_SELL:
        	size = max(1,round(trader.get_best_price(ticker).get_ask_size() / 5)) # Only sell as much as you can buy back. Divide by 5 to decrease risk. At least 1
        	price = ask-spreadWiden # Can sell below ask if wide spread, or above ask if high volume
        
        order = shift.Order(orderType, ticker, size, price)
        trader.submit_order(order)
        #print(orderType, size, ticker, "@", price)

        # Give the order time to fill
        waitCount = 1
        while trader.get_order(order.id).status != shift.Order.Status.FILLED and waitCount <= fillTime and trader.get_order(order.id).status != shift.Order.Status.REJECTED:
            #print(waitCount, ticker, "Status:",trader.get_order(order.id).status)
            time.sleep(.1)
            waitCount = waitCount + 1
        #print(waitCount, trader.get_order(order.id).status)

        # Cancel the buy order if never filled and was not rejected
        if trader.get_order(order.id).status != shift.Order.Status.REJECTED and trader.get_order(order.id).status != shift.Order.Status.FILLED:
            trader.submit_cancellation(order)
            #print("Cancelled", ticker)


        rightNow =  trader.get_last_trade_time() # Reset datetime of right now

    # 30 minutes till end of trading day
    closePositions(trader, ticker)

    # Done trading
    return