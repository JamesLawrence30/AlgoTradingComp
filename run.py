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
sys.path.insert(1, './functions')
from firstStrategy import firstStrategy
from marketMaker import marketMaker

def main(argv):

    # Create trader object
    trader = shift.Trader(credentials.user) # **Change to competition user****************************************

    # Connect and subscribe to all available order books
    try:
        trader.connect("initiator.cfg", credentials.password) # **Change to competition password*****************************
        trader.sub_all_order_book() # Subscribe to orderbook for all tickers.  Can also choose one particular stock
    except shift.IncorrectPasswordError as e:
        print(e)
    except shift.ConnectionTimeoutError as e:
        print(e)

    time.sleep(.5)
    # Date of simulation
    today = trader.get_last_trade_time().date()

    # End of trading day datetime
    endTime = dt.time(16,59,0) # **Competition time********************************
    #endTime = dt.time(10,16,30) # **Set time for development**
    dayEnd = dt.datetime.combine(today,endTime)

    # Begin trading
    print("Initial buying power:",trader.get_portfolio_summary().get_total_bp())

    #ticker = "SPY"
    #firstStrategy(trader, ticker, dayEnd, 5.0)

    ticker = "CSCO"
    marketMaker(trader, ticker, dayEnd, 3, 30, 0.00) # Lag, Max fill time, Difference from bid/ask ( - contracts spread, + increases spread)
    """
    marketMaker(trader, "CSCO", dayEnd, 3, 30, 0.00) ***
    marketMaker(trader, "BA", dayEnd, 3, 30, -0.02)
    marketMaker(trader, "TRV", dayEnd, 3, 30, 0.01)
    marketMaker(trader, "UNH", dayEnd, 3, 30, 0.01)
    """
    
    # Disconnect
    print("Final buying power:",trader.get_portfolio_summary().get_total_bp())
    trader.disconnect()

    return

if __name__ == "__main__":
    main(sys.argv)
