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

def marketMaker(trader: shift.Trader, ticker, dayEnd, lag=3, fillTime=20, spreadWiden=0.00):

    # Datetime of simulation
    rightNow =  trader.get_last_trade_time()

    fillTime = fillTime*10
    count = 1
    # While the time is before end of day...
    while(dayEnd > rightNow):
        print(rightNow, "Total P/L:",trader.get_portfolio_summary().get_total_realized_pl())
        """
        Make Trades Here:
        """
        if count % (lag*3) == 0 or trader.get_portfolio_summary().get_total_bp() < 150000: # Every so often, sell off inventory.  Wait longer if lower lag ((1/lag)*15)
        	closePositions(trader) # Free up buying power and reduce risk
        	print("Sold inventory, risk & bp reset")

        time.sleep(lag) # Give prices some time to change

        # Submit a buy order
        buySize = round(trader.get_best_price(ticker).get_ask_size() / 3) # Only buy as much as you can sell. Divide by 3 so buying power lasts on high volume
        buyPrice = trader.get_best_price(ticker).get_bid_price()-spreadWiden # Can buy above bid with wide spread, or below bid if high volume
        limit_buy = shift.Order(shift.Order.Type.LIMIT_BUY, ticker, buySize, buyPrice)
        trader.submit_order(limit_buy)
        print("Buy", buySize, "@", buyPrice)

        # Give the order time to fill
        waitCount = 1
        while trader.get_order(limit_buy.id).status != shift.Order.Status.FILLED and waitCount <= fillTime and trader.get_order(limit_buy.id).status != shift.Order.Status.REJECTED:
            print(waitCount, "Status:",trader.get_order(limit_buy.id).status)
            time.sleep(.1)
            waitCount = waitCount + 1

        print(waitCount, trader.get_order(limit_buy.id).status)

        # Sell if the buy order filled and the sale is be profitable
        sellPrice = trader.get_best_price(ticker).get_ask_price()+spreadWiden # Can sell below ask with wide spread, or above ask if high volume
        if trader.get_order(limit_buy.id).status == shift.Order.Status.FILLED:
        	if sellPrice > buyPrice: # Sell now for profit
        		limit_sell = shift.Order(shift.Order.Type.LIMIT_SELL, ticker, buySize, sellPrice)
        		trader.submit_order(limit_sell)
        		print("Sell all @", sellPrice)
        	else:
        		# List for sale and Hold as inventory for now, do not market sell for an immediate loss
                # 	Note: holding inventory reduces buying power, can lead to rejected orders
        		limit_sell = shift.Order(shift.Order.Type.LIMIT_SELL, ticker, buySize, buyPrice)
        		trader.submit_order(limit_sell)
        		print("Resell all @", buyPrice)

        # Sell partially filled orders if profitable
        elif trader.get_order(limit_buy.id).status == shift.Order.Status.PARTIALLY_FILLED:
        	for order in trader.get_executed_orders(limit_buy.id):
        		if sellPrice > order.executed_price: # Sell now for profit
        			limit_sell = shift.Order(shift.Order.Type.LIMIT_SELL, ticker, order.executed_size, sellPrice)
        			trader.submit_order(limit_sell)
        			print("Sell", order.executed_size, "@", sellPrice)
        		else:
        			# List for sale and Hold as inventory for now, do not market sell for an immediate loss
                    # 	Note: holding inventory reduces buying power, can lead to rejected orders
        			limit_sell = shift.Order(shift.Order.Type.LIMIT_SELL, ticker, order.executed_size, order.executed_price)
        			trader.submit_order(limit_sell)
        			print("Resell", order.executed_size, "@", order.executed_price)

        # Cancel the buy order if never filled and was not rejected
        elif trader.get_order(limit_buy.id).status != shift.Order.Status.REJECTED:
            trader.submit_cancellation(limit_buy)
            print("Cancelled")

        # Monitor inventory and sell off risk
        """!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! **TODO**
        checkInventory(trader)
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"""

        count = count + 1 # Increment counter
        rightNow =  trader.get_last_trade_time() # Reset datetime of right now

    # 60 seconds till end of trading day
    closePositions(trader)

    # Done trading
    return