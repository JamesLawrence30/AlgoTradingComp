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
from checkInventory import checkInventory

def marketMaker(trader: shift.Trader, ticker, dayEnd, allocation, lag=3, fillTime=20, spreadWiden=0.00):

    # Datetime of simulation
    rightNow =  trader.get_last_trade_time()

    fillTime = fillTime*10
    count = 1
    # While the time is before end of day...
    while(dayEnd > rightNow):
        time.sleep(lag) # Give prices some time to change
        print("P/L:",trader.get_portfolio_summary().get_total_realized_pl())
        """
        Make Trades Here:
        """
        onHand = trader.get_portfolio_item(ticker).get_shares()*((trader.get_best_price(ticker).get_bid_price()+trader.get_best_price(ticker).get_ask_price())/2) # Portfolio value of the stock
        maxAllowed = allocation*(1000000 + trader.get_portfolio_summary().get_total_realized_pl()) # Maximum portfolio allocation for this stock
        print(ticker, "on hand:", onHand, "max:", maxAllowed)
        if onHand > maxAllowed:
            closePositions(trader, ticker, onHand, maxAllowed) # Free up buying power and reduce risk
            continue
        elif onHand < 0:
            closePositions(trader, ticker) # Cover unexpected short positions!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            continue

        time.sleep(lag) # Give prices some time to change

        # Monitor inventory and sell off risk
        ####Maybe do something with timedelta to make this check occur every 10 minutes, then set current time to new base to add 10 min to
        ###Also include a check if onHand value has changed +/- 2% to sell off inventory
        #checkInventory(trader, ticker)#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        # Submit a buy order
        buySize = max(1,round(trader.get_best_price(ticker).get_ask_size() / 5)) # Only buy as much as you can sell. Divide by 3 so buying power lasts on high volume. At least 2
        buyPrice = trader.get_best_price(ticker).get_bid_price()-spreadWiden # Can buy above bid with wide spread, or below bid if high volume
        limit_buy = shift.Order(shift.Order.Type.LIMIT_BUY, ticker, buySize, buyPrice)
        trader.submit_order(limit_buy)
        print("Buy", buySize, ticker, "@", buyPrice)

        # Give the order time to fill
        waitCount = 1
        while trader.get_order(limit_buy.id).status != shift.Order.Status.FILLED and waitCount <= fillTime and trader.get_order(limit_buy.id).status != shift.Order.Status.REJECTED:
            #print(waitCount, ticker, "Status:",trader.get_order(limit_buy.id).status)
            time.sleep(.1)
            waitCount = waitCount + 1

        #print(waitCount, trader.get_order(limit_buy.id).status)

        # Sell if the buy order filled and the sale is be profitable
        sellPrice = trader.get_best_price(ticker).get_ask_price()+spreadWiden # Can sell below ask with wide spread, or above ask if high volume
        if trader.get_order(limit_buy.id).status == shift.Order.Status.FILLED:
        	if sellPrice > buyPrice: # Sell now for profit
        		limit_sell = shift.Order(shift.Order.Type.LIMIT_SELL, ticker, buySize, sellPrice)
        		trader.submit_order(limit_sell)
        		print("Sell all", ticker, "@", sellPrice)
        		count = count - 2 # lower count if active
        	else:
        		# List for sale and Hold as inventory for now, do not market sell for an immediate loss
                # 	Note: holding inventory reduces buying power, can lead to rejected orders
        		limit_sell = shift.Order(shift.Order.Type.LIMIT_SELL, ticker, buySize, buyPrice)
        		trader.submit_order(limit_sell)
        		print("Resell all", ticker, "@", buyPrice)

        # Sell partially filled orders if profitable
        elif trader.get_order(limit_buy.id).status == shift.Order.Status.PARTIALLY_FILLED:
        	for order in trader.get_executed_orders(limit_buy.id):
        		if sellPrice > order.executed_price: # Sell now for profit
        			limit_sell = shift.Order(shift.Order.Type.LIMIT_SELL, ticker, order.executed_size, sellPrice)
        			trader.submit_order(limit_sell)
        			print("Sell", order.executed_size, ticker, "@", sellPrice)
        			count = count - 2 # lower count if active
        		else:
        			# List for sale and Hold as inventory for now, do not market sell for an immediate loss
                    # 	Note: holding inventory reduces buying power, can lead to rejected orders
        			limit_sell = shift.Order(shift.Order.Type.LIMIT_SELL, ticker, order.executed_size, order.executed_price)
        			trader.submit_order(limit_sell)
        			print("Resell", order.executed_size, ticker, "@", order.executed_price)

        # Cancel the buy order if never filled and was not rejected
        elif trader.get_order(limit_buy.id).status != shift.Order.Status.REJECTED:
            trader.submit_cancellation(limit_buy)
            print("Cancelled", ticker)
        

        count = count + 1 # Increment counter
        rightNow =  trader.get_last_trade_time() # Reset datetime of right now

    # 60 seconds till end of trading day
    closePositions(trader, ticker)

    # Done trading
    return