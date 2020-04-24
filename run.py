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
    """
    trader.request_sample_prices(["CS1", "CS2"], 5.0, 26) # Ticker list, sample freq, sample window size !!!!!!!!!!!
    """

    # Wait for 30 minutes
    trafficLight(trader, dayStart, 2.0)

    # End of trading day datetime
    endTime = dt.time(15,50,0) # Competition time
    dayEnd = dt.datetime.combine(today,endTime)

    # Begin trading
    print("Initial buying power:",trader.get_portfolio_summary().get_total_bp())

    # View destination exchange(s) for each ticker
    seeExchange(trader, "CS1")
    seeExchange(trader, "CS2")
    
    # Stop loss / take profit
    manageInvCS1 = threading.Thread(target=manageInventory, args=[trader, 'CS1', dayEnd], name='manageInvCS1')
    manageInvCS2 = threading.Thread(target=manageInventory, args=[trader, 'CS2', dayEnd], name='manageInvCS2')

    # ---TECHNICAL ANALYSIS STRATEGY--- threads
    """
    longTechCS1 = threading.Thread(target=technicalStrat, args=[trader, "CS1", True, dayEnd, 1.0], name='longTechCS1')
    shortTechCS1 = threading.Thread(target=technicalStrat, args=[trader, "CS1", False, dayEnd, 1.0], name='shortTechCS1')

    longTechCS2 = threading.Thread(target=technicalStrat, args=[trader, "CS2", True, dayEnd, 1.0], name='longTechCS2')
    shortTechCS2 = threading.Thread(target=technicalStrat, args=[trader, "CS2", False, dayEnd, 1.0], name='shortTechCS2')
    """

    
    # ---MARKET MAKER STRATEGY--- threads
    #******allocation should now be max % at risk******#
    longCS1_1 = threading.Thread(target=marketMaker, args=[trader, 'CS1', dayEnd, .15, shift.Order.Type.LIMIT_BUY, 3, 30, 0.08], name='longCS1_1')
    longCS1_2 = threading.Thread(target=marketMaker, args=[trader, 'CS1', dayEnd, .15, shift.Order.Type.LIMIT_BUY, 3, 30, 0.08], name='longCS1_2')
    longCS1_3 = threading.Thread(target=marketMaker, args=[trader, 'CS1', dayEnd, .15, shift.Order.Type.LIMIT_BUY, 3, 30, 0.08], name='longCS1_3')
    longCS1_4 = threading.Thread(target=marketMaker, args=[trader, 'CS1', dayEnd, .15, shift.Order.Type.LIMIT_BUY, 3, 30, 0.08], name='longCS1_4')

    longCS2_1 = threading.Thread(target=marketMaker, args=[trader, 'CS2', dayEnd, .15, shift.Order.Type.LIMIT_BUY, 3, 30, 0.08], name='longCS2_1')
    longCS2_2 = threading.Thread(target=marketMaker, args=[trader, 'CS2', dayEnd, .15, shift.Order.Type.LIMIT_BUY, 3, 30, 0.08], name='longCS2_2')
    longCS2_3 = threading.Thread(target=marketMaker, args=[trader, 'CS2', dayEnd, .15, shift.Order.Type.LIMIT_BUY, 3, 30, 0.08], name='longCS2_3')
    longCS2_4 = threading.Thread(target=marketMaker, args=[trader, 'CS2', dayEnd, .15, shift.Order.Type.LIMIT_BUY, 3, 30, 0.08], name='longCS2_4')


    shortCS1_1 = threading.Thread(target=marketMaker, args=[trader, 'CS1', dayEnd, .15, shift.Order.Type.LIMIT_SELL, 3, 30, 0.08], name='shortCS1_1')
    shortCS1_2 = threading.Thread(target=marketMaker, args=[trader, 'CS1', dayEnd, .15, shift.Order.Type.LIMIT_SELL, 3, 30, 0.08], name='shortCS1_2')
    shortCS1_3 = threading.Thread(target=marketMaker, args=[trader, 'CS1', dayEnd, .15, shift.Order.Type.LIMIT_SELL, 3, 30, 0.08], name='shortCS1_3')
    shortCS1_4 = threading.Thread(target=marketMaker, args=[trader, 'CS1', dayEnd, .15, shift.Order.Type.LIMIT_SELL, 3, 30, 0.08], name='shortCS1_4')

    shortCS2_1 = threading.Thread(target=marketMaker, args=[trader, 'CS2', dayEnd, .15, shift.Order.Type.LIMIT_SELL, 3, 30, 0.08], name='shortCS2_1')
    shortCS2_2 = threading.Thread(target=marketMaker, args=[trader, 'CS2', dayEnd, .15, shift.Order.Type.LIMIT_SELL, 3, 30, 0.08], name='shortCS2_2')
    shortCS2_3 = threading.Thread(target=marketMaker, args=[trader, 'CS2', dayEnd, .15, shift.Order.Type.LIMIT_SELL, 3, 30, 0.08], name='shortCS2_3')
    shortCS2_4 = threading.Thread(target=marketMaker, args=[trader, 'CS2', dayEnd, .15, shift.Order.Type.LIMIT_SELL, 3, 30, 0.08], name='shortCS2_4')


    # --Initiate threads--
    manageInvCS1.start()
    manageInvCS2.start()

    """
    longTechCS1.start()
    shortTechCS1.start()

    longTechCS2.start()
    shortTechCS2.start()
    """

    longCS1_1.start()
    shortCS1_1.start()
    longCS2_1.start()
    shortCS2_1.start()
    time.sleep(5)

    longCS1_2.start()
    shortCS1_2.start()
    longCS2_2.start()
    shortCS2_2.start()
    time.sleep(5)

    longCS1_3.start()
    shortCS1_3.start()
    longCS2_3.start()
    shortCS2_3.start()
    time.sleep(5)

    longCS1_4.start()
    shortCS1_4.start()
    longCS2_4.start()
    shortCS2_4.start()
    time.sleep(5)


    # --Execute functions on threads-- 
    manageInvCS1.join()
    manageInvCS2.join()

    """
    longTechCS1.join()
    shortTechCS1.join()

    longTechCS2.join()
    shortTechCS2.join()
    """

    longCS1_1.join()
    shortCS1_1.join()
    longCS2_1.join()
    shortCS2_1.join()

    longCS1_2.join()
    shortCS1_2.join()
    longCS2_2.join()
    shortCS2_2.join()

    longCS1_3.join()
    shortCS1_3.join()
    longCS2_3.join()
    shortCS2_3.join()

    longCS1_4.join()
    shortCS1_4.join()
    longCS2_4.join()
    shortCS2_4.join()


    # Disconnect
    time.sleep(60) # Wait for all threads to sell inventory
    print("Final buying power:",trader.get_portfolio_summary().get_total_bp())
    trader.disconnect()

    return

if __name__ == "__main__":
    main(sys.argv)
