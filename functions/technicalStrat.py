# ---------------------------------------------------------------------------------------------------------------
# Property of Two and Twenty LLP
# ---------------------------------------------------------------------------------------------------------------

# Imported Libraries
import time
import pandas as pd
import numpy as np
import datetime as dt
import shift

# Imported Functions
from closePositions import closePositions
from manageInventory import manageInventory

def technicalStrat(trader: shift.Trader, ticker, lastTradeSell, dayEnd, lag=1):

    rightNow =  trader.get_last_trade_time() # Datetime of simulation

    # While the time is before end of day...
    while(dayEnd > rightNow):
        print("P/L:",trader.get_portfolio_summary().get_total_realized_pl(), " Waiting list:", trader.get_waiting_list_size())
        """
        Make Trades Here:
        """
        priceSeries = pd.Series(trader.get_sample_prices(ticker, True)) # ticker, mid-prices
        time.sleep(lag) # Give prices some time to change

        if priceSeries.size == 26:
	        mShort = priceSeries.ewm(span=12, adjust=False).mean() # 12 period EMA
	        mLong = priceSeries.ewm(span=26, adjust=False).mean() # 26 period EMA
	        MACD = mShort-mLong # Calculate convergence and divergence

	        mSignal = MACD.ewm(span=9, adjust=False).mean() # 9 period EMA signal line

	        mHist = MACD-mSignal # Trade signal producer

	        
	        SMA = priceSeries[:19].mean() # 20 second simple moving average
	        if lastTradeSell == True:
	        	bUpper = SMA + (priceSeries[:19].std()*3.0) # Upper Bollinger Band
	        	bLower = SMA - (priceSeries[:19].std()*1.5) # Low Bollinger Band - more lenient, safer sell
	        else:
	        	bUpper = SMA + (priceSeries[:19].std()*1.5) # Upper Bollinger Band - more lenient, safer cover
	        	bLower = SMA - (priceSeries[:19].std()*3.0) # Low Bollinger Band
	        #######!!!!!!possibly have a second band outside first..for too strong movement!!!!!!!!!!!!!!!!!!!!!!!!!!!!


	        # Open long position / Cover short position
	        if lastTradeSell == True and mHist.iloc[-1] > 0 and trader.get_close_price(ticker, True, 1) > bUpper: # ticker, Buy, Size
	            """
	            buySize = max(1,round(trader.get_best_price(ticker).get_ask_size() / 5)) # Only buy as much as can sell. Divide so bp lasts on high volume. At least 1
	            openLong = shift.Order(shift.Order.Type.MARKET_BUY, ticker, buySize)
	            """
	            
	            for i in range(1,20): # seems too slow..
	            	openLong = shift.Order(shift.Order.Type.MARKET_BUY, ticker, 1)
	            	trader.submit_order(openLong)
	            
	            print("Buy", ticker)
	            lastTradeSell = False

	        # Close long positions for now / Open short position
	        elif lastTradeSell == False and mHist.iloc[-1] < 0 and trader.get_close_price(ticker, False, 1) < bLower: # ticker, Sell, Size
	            """
	            item = trader.get_portfolio_item(ticker) # Check this stock in our portfolio
	            if item.get_shares() > 0: # Sell if we have shares
	            	sellSize = int(item.get_shares() / 100)
	            	closeLong = shift.Order(shift.Order.Type.MARKET_SELL, ticker, sellSize) # Order size in 100's of shares, strictly as an int
	            	trader.submit_order(closeLong)
	            """
	            
	            for i in range(1,20): # seems too slow..
	            	closeLong = shift.Order(shift.Order.Type.MARKET_SELL, ticker, 1)
	            	trader.submit_order(closeLong)
	            
	            print("Sell", ticker)
	            lastTradeSell = True

	        item = trader.get_portfolio_item(ticker)
	        if item.get_shares() != 0:
	        	manageInventory(trader, ticker, item)


        rightNow =  trader.get_last_trade_time() # Reset datetime of right now

    # 60 seconds till end of trading day
    trader.cancel_all_sample_prices_requests() # Stop sampling prices on threads
    closePositions(trader, ticker) # Close out open positions so we don't get fined

    # Done trading
    return