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
import threading

# Imported Functions
sys.path.insert(1, './functions')
from firstStrategy import firstStrategy
from marketMaker import marketMaker
from trafficLight import trafficLight
from technicalStrat import technicalStrat

def main(argv):

    # Create trader object
    trader = shift.Trader(credentials.user) # **Change to competition user***********************************************************

    # Connect and subscribe to all available order books
    try:
        trader.connect("initiator.cfg", credentials.password) # **Change to competition password*************************************
        #trader.sub_all_order_book() # Subscribe to orderbook for all tickers.  Can also choose one particular stock
        trader.sub_order_book("SPY")#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!**************************!!!!!!!!!!!!!!!!!
    except shift.IncorrectPasswordError as e:
        print(e)
    except shift.ConnectionTimeoutError as e:
        print(e)

    time.sleep(5)
    # Date of simulation
    today = trader.get_last_trade_time().date()

    startTime = dt.time(9,30,0) # Competition time
    dayStart = dt.datetime.combine(today,startTime)

    # Wait for 30 minutes
    trafficLight(trader, dayStart, 2.0)

    # End of trading day datetime
    endTime = dt.time(15,55,0) # Competition time!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    dayEnd = dt.datetime.combine(today,endTime)

    #Begin collecting prices
    trader.request_sample_prices(["SPY"], 2.0, 26) # Ticker list, sample freq, sample window size

    # Begin trading
    print("Initial buying power:",trader.get_portfolio_summary().get_total_bp())



    #!!!!!!***SHORT VIXY TO HEDGE AGAINST LOW VOLATILITY DEGRADING STRATEGY***!!!!!
    
    SPYlong = threading.Thread(target=technicalStrat, args=[trader, "SPY", True, dayEnd, 1.0], name='SPYlong')
    SPYshort = threading.Thread(target=technicalStrat, args=[trader, "SPY", False, dayEnd, 1.0], name='SPYshort')
    #XOM1 = threading.Thread(target=technicalStrat, args=[trader, "XOM", dayEnd, 1.0], name='XOM1')
    #JPM1 = threading.Thread(target=technicalStrat, args=[trader, "JPM", dayEnd, 1.0], name='JPM1')
    #KO1 = threading.Thread(target=technicalStrat, args=[trader, "KO", dayEnd, 1.0], name='KO1')
    #MRK1 = threading.Thread(target=technicalStrat, args=[trader, "MRK", dayEnd, 1.0], name='MRK1')
    #PG1 = threading.Thread(target=technicalStrat, args=[trader, "PG", dayEnd, 1.0], name='PG1')
    #PFE1 = threading.Thread(target=technicalStrat, args=[trader, "PFE", dayEnd, 1.0], name='PFE1')
    #WBA1 = threading.Thread(target=technicalStrat, args=[trader, "WBA", dayEnd, 1.0], name='WBA1')
    

    SPYlong.start()
    SPYshort.start()
    #XOM1.start()
    #JPM1.start()
    #KO1.start()
    #MRK1.start()
    #PG1.start()
    #PFE1.start()
    #WBA1.start()
    #SPY2.start()
    

    SPYlong.join()
    SPYshort.join()
    #XOM1.join()
    #JPM1.join()
    #KO1.join()
    #MRK1.join()
    #PG1.join()
    #PFE1.join()
    #WBA1.join()
    #SPY2.join()

    # Disconnect
    time.sleep(59) # Wait for all threads to sell inventory
    print("Final waiting list size: " + str(trader.get_waiting_list_size()))
    print("Final buying power:",trader.get_portfolio_summary().get_total_bp())
    trader.disconnect()

    return

if __name__ == "__main__":
    main(sys.argv)
