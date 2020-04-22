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
from marketMaker import marketMaker
from trafficLight import trafficLight
from manageInventory import manageInventory
from technicalStrat import technicalStrat
from seeExchange import seeExchange

def main(argv):

    # Create trader object
    trader = shift.Trader(credentials.user) # **Change to competition user***********************************************************

    # Connect and subscribe to all available order books
    try:
        trader.connect("initiator.cfg", credentials.password) # **Change to competition password*************************************
        #trader.sub_all_order_book() # Subscribe to orderbook for all tickers.  Can also choose one particular stock
        trader.sub_order_book("CS1")
        trader.sub_order_book("CS2")
    except shift.IncorrectPasswordError as e:
        print(e)
    except shift.ConnectionTimeoutError as e:
        print(e)

    time.sleep(10)
    # Date of simulation
    today = trader.get_last_trade_time().date()

    startTime = dt.time(9,30,30) # Competition time
    dayStart = dt.datetime.combine(today,startTime)

    #Begin collecting prices
    trader.request_sample_prices(["CS1", "CS2"], 5.0, 26) # Ticker list, sample freq, sample window size !!!!!!!!!!!

    # Wait for 30 minutes
    trafficLight(trader, dayStart, 2.0)

    # End of trading day datetime
    endTime = dt.time(15,50,0) # Competition time
    dayEnd = dt.datetime.combine(today,endTime)

    # Begin trading
    print("Initial buying power:",trader.get_portfolio_summary().get_total_bp())

    
    # Stop loss / take profit
    manageInvCS1 = threading.Thread(target=manageInventory, args=[trader, 'CS1', dayEnd], name='manageInvCS1')
    manageInvCS2 = threading.Thread(target=manageInventory, args=[trader, 'CS2', dayEnd], name='manageInvCS2')

    # ---TECHNICAL ANALYSIS STRATEGY--- threads
    longTechCS1 = threading.Thread(target=technicalStrat, args=[trader, "CS1", True, dayEnd, 1.0], name='longTechCS1')
    shortTechCS1 = threading.Thread(target=technicalStrat, args=[trader, "CS1", False, dayEnd, 1.0], name='shortTechCS1')

    longTechCS2 = threading.Thread(target=technicalStrat, args=[trader, "CS2", True, dayEnd, 1.0], name='longTechCS2')
    shortTechCS2 = threading.Thread(target=technicalStrat, args=[trader, "CS2", False, dayEnd, 1.0], name='shortTechCS2')

    seeExchange(trader, "CS1")
    seeExchange(trader, "CS2")
    
    # ---MARKET MAKER STRATEGY--- threads
    #******allocation should now be max risk******#
    """
    longBA1 = threading.Thread(target=marketMaker, args=[trader, 'BA', dayEnd, .25, shift.Order.Type.LIMIT_BUY, 3, 30, 0.08], name='longBA1')
    longBA2 = threading.Thread(target=marketMaker, args=[trader, 'BA', dayEnd, .25, shift.Order.Type.LIMIT_BUY, 3, 30, 0.08], name='longBA2')
    longBA3 = threading.Thread(target=marketMaker, args=[trader, 'BA', dayEnd, .25, shift.Order.Type.LIMIT_BUY, 3, 30, 0.08], name='longBA3')
    longBA4 = threading.Thread(target=marketMaker, args=[trader, 'BA', dayEnd, .25, shift.Order.Type.LIMIT_BUY, 3, 30, 0.08], name='longBA4')

    shortBA1 = threading.Thread(target=marketMaker, args=[trader, 'BA', dayEnd, .25, shift.Order.Type.LIMIT_SELL, 3, 30, 0.08], name='shortBA1')
    shortBA2 = threading.Thread(target=marketMaker, args=[trader, 'BA', dayEnd, .25, shift.Order.Type.LIMIT_SELL, 3, 30, 0.08], name='shortBA2')
    shortBA3 = threading.Thread(target=marketMaker, args=[trader, 'BA', dayEnd, .25, shift.Order.Type.LIMIT_SELL, 3, 30, 0.08], name='shortBA3')
    shortBA4 = threading.Thread(target=marketMaker, args=[trader, 'BA', dayEnd, .25, shift.Order.Type.LIMIT_SELL, 3, 30, 0.08], name='shortBA4')
    """

    # --Initiate threads--
    manageInvCS1.start()
    manageInvCS2.start()


    longTechCS1.start()
    shortTechCS1.start()

    longTechCS2.start()
    shortTechCS2.start()


    """
    longBA1.start()
    shortBA1.start()
    time.sleep(5)

    longBA2.start()
    shortBA2.start()
    time.sleep(5)

    longBA3.start()
    shortBA3.start()
    time.sleep(5)

    longBA4.start()
    shortBA4.start()
    time.sleep(5)
    """

    # --Execute functions on threads-- 
    manageInvCS1.join()
    manageInvCS2.join()


    longTechCS1.join()
    shortTechCS1.join()

    longTechCS2.join()
    shortTechCS2.join()


    """
    longBA1.join()
    shortBA1.join()

    longBA2.join()
    shortBA2.join()

    longBA3.join()
    shortBA3.join()

    longBA4.join()
    shortBA4.join()
    """


    # Disconnect
    time.sleep(60) # Wait for all threads to sell inventory
    print("Final buying power:",trader.get_portfolio_summary().get_total_bp())
    trader.disconnect()

    return

if __name__ == "__main__":
    main(sys.argv)
