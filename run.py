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

def main(argv):

    # Create trader object
    trader = shift.Trader(credentials.user) # **Change to competition user***********************************************************

    # Connect and subscribe to all available order books
    try:
        trader.connect("initiator.cfg", credentials.password) # **Change to competition password*************************************
        trader.sub_all_order_book() # Subscribe to orderbook for all tickers.  Can also choose one particular stock
    except shift.IncorrectPasswordError as e:
        print(e)
    except shift.ConnectionTimeoutError as e:
        print(e)

    time.sleep(5)
    # Date of simulation
    today = trader.get_last_trade_time().date()

    startTime = dt.time(10,0,0) # Competition time
    dayStart = dt.datetime.combine(today,startTime)

    # Wait for 30 minutes
    trafficLight(trader, dayStart, 2.0)

    # End of trading day datetime
    endTime = dt.time(15,30,0) # Competition time
    dayEnd = dt.datetime.combine(today,endTime)

    # Begin trading
    print("Initial buying power:",trader.get_portfolio_summary().get_total_bp())

    """
    # ---RATE OF CHANGE STRATEGY--- threads
    cscoMACD = threading.Thread(target=firstStrategy, args=[trader, 'CSCO', dayEnd, 1.0, 8, 0.00], name='cscoMACD')
    vixyMACD = threading.Thread(target=firstStrategy, args=[trader, 'VIXY', dayEnd, 1.0, 8, 0.00], name='vixyMACD')
    spyMACD = threading.Thread(target=firstStrategy, args=[trader, 'SPY', dayEnd, 1.0, 8, 0.00], name='spyMACD')

    # Initiate threads
    cscoMACD.start()
    vixyMACD.start()
    spyMACD.start()

    # Execute functions on threads
    cscoMACD.join()
    vixyMACD.join()
    spyMACD.join()
    """
    
    # ---MARKET MAKER STRATEGY--- threads
    
    trv1MRKTMKR = threading.Thread(target=marketMaker, args=[trader, 'TRV', dayEnd, .85, 3, 30, -0.01], name='trv1MRKTMKR')
    trv2MRKTMKR = threading.Thread(target=marketMaker, args=[trader, 'TRV', dayEnd, .85, 3, 30, 0.00], name='trv2MRKTMKR')
    trv3MRKTMKR = threading.Thread(target=marketMaker, args=[trader, 'TRV', dayEnd, .85, 3, 30, -0.01], name='trv3MRKTMKR')
    trv4MRKTMKR = threading.Thread(target=marketMaker, args=[trader, 'TRV', dayEnd, .85, 3, 30, 0.00], name='trv4MRKTMKR')
    trv5MRKTMKR = threading.Thread(target=marketMaker, args=[trader, 'TRV', dayEnd, .85, 3, 30, -0.01], name='trv5MRKTMKR')
    trv6MRKTMKR = threading.Thread(target=marketMaker, args=[trader, 'TRV', dayEnd, .85, 3, 30, 0.00], name='trv6MRKTMKR')
    trv7MRKTMKR = threading.Thread(target=marketMaker, args=[trader, 'TRV', dayEnd, .85, 3, 30, -0.01], name='trv7MRKTMKR')
    trv8MRKTMKR = threading.Thread(target=marketMaker, args=[trader, 'TRV', dayEnd, .85, 3, 30, 0.00], name='trv8MRKTMKR')
    """
    ba1MRKTMKR = threading.Thread(target=marketMaker, args=[trader, 'BA', dayEnd, .8, 3, 30, -0.02], name='ba1MRKTMKR')
    ba2MRKTMKR = threading.Thread(target=marketMaker, args=[trader, 'BA', dayEnd, .8, 3, 30, -0.02], name='ba2MRKTMKR')
    ba3MRKTMKR = threading.Thread(target=marketMaker, args=[trader, 'BA', dayEnd, .8, 3, 30, -0.02], name='ba3MRKTMKR')
    ba4MRKTMKR = threading.Thread(target=marketMaker, args=[trader, 'BA', dayEnd, .8, 3, 30, -0.02], name='ba4MRKTMKR')
    ba5MRKTMKR = threading.Thread(target=marketMaker, args=[trader, 'BA', dayEnd, .8, 3, 30, -0.02], name='ba5MRKTMKR')
    ba6MRKTMKR = threading.Thread(target=marketMaker, args=[trader, 'BA', dayEnd, .8, 3, 30, -0.02], name='ba6MRKTMKR')
    """
    """
    spy1MRKTMKR = threading.Thread(target=marketMaker, args=[trader, 'SPY', dayEnd, .8, 3, 30, 0.00], name='spy1MRKTMKR')
    spy2MRKTMKR = threading.Thread(target=marketMaker, args=[trader, 'SPY', dayEnd, .8, 3, 30, 0.00], name='spy2MRKTMKR')
    spy3MRKTMKR = threading.Thread(target=marketMaker, args=[trader, 'SPY', dayEnd, .8, 3, 30, 0.00], name='spy3MRKTMKR')
    spy4MRKTMKR = threading.Thread(target=marketMaker, args=[trader, 'SPY', dayEnd, .8, 3, 30, 0.00], name='spy4MRKTMKR')
    spy5MRKTMKR = threading.Thread(target=marketMaker, args=[trader, 'SPY', dayEnd, .8, 3, 30, 0.00], name='spy5MRKTMKR')
    spy6MRKTMKR = threading.Thread(target=marketMaker, args=[trader, 'SPY', dayEnd, .8, 3, 30, 0.00], name='spy6MRKTMKR')
    """
    """
    ko1MRKTMKR = threading.Thread(target=marketMaker, args=[trader, 'KO', dayEnd, .8, 3, 30, 0.00], name='ko1MRKTMKR')
    ko2MRKTMKR = threading.Thread(target=marketMaker, args=[trader, 'KO', dayEnd, .8, 3, 30, 0.00], name='ko2MRKTMKR')
    ko3MRKTMKR = threading.Thread(target=marketMaker, args=[trader, 'KO', dayEnd, .8, 3, 30, 0.00], name='ko3MRKTMKR')
    ko4MRKTMKR = threading.Thread(target=marketMaker, args=[trader, 'KO', dayEnd, .8, 3, 30, 0.00], name='ko4MRKTMKR')
    ko5MRKTMKR = threading.Thread(target=marketMaker, args=[trader, 'KO', dayEnd, .8, 3, 30, 0.00], name='ko5MRKTMKR')
    ko6MRKTMKR = threading.Thread(target=marketMaker, args=[trader, 'KO', dayEnd, .8, 3, 30, 0.00], name='ko6MRKTMKR')
    """
    """
    csco1MRKTMKR = threading.Thread(target=marketMaker, args=[trader, 'CSCO', dayEnd, .8, 3, 30, 0.00], name='csco1MRKTMKR')
    csco2MRKTMKR = threading.Thread(target=marketMaker, args=[trader, 'CSCO', dayEnd, .8, 3, 30, 0.00], name='csco2MRKTMKR')
    csco3MRKTMKR = threading.Thread(target=marketMaker, args=[trader, 'CSCO', dayEnd, .8, 3, 30, 0.00], name='csco3MRKTMKR')
    csco4MRKTMKR = threading.Thread(target=marketMaker, args=[trader, 'CSCO', dayEnd, .8, 3, 30, 0.00], name='csco4MRKTMKR')
    csco5MRKTMKR = threading.Thread(target=marketMaker, args=[trader, 'CSCO', dayEnd, .8, 3, 30, 0.00], name='csco5MRKTMKR')
    csco6MRKTMKR = threading.Thread(target=marketMaker, args=[trader, 'CSCO', dayEnd, .8, 3, 30, 0.00], name='csco6MRKTMKR')
    """
    """
    vixy1MRKTMKR = threading.Thread(target=marketMaker, args=[trader, 'VIXY', dayEnd, .8, 3, 30, 0.00], name='vixy1MRKTMKR')
    vixy2MRKTMKR = threading.Thread(target=marketMaker, args=[trader, 'VIXY', dayEnd, .8, 3, 30, 0.00], name='vixy2MRKTMKR')
    vixy3MRKTMKR = threading.Thread(target=marketMaker, args=[trader, 'VIXY', dayEnd, .8, 3, 30, 0.00], name='vixy3MRKTMKR')
    vixy4MRKTMKR = threading.Thread(target=marketMaker, args=[trader, 'VIXY', dayEnd, .8, 3, 30, 0.00], name='vixy4MRKTMKR')
    vixy5MRKTMKR = threading.Thread(target=marketMaker, args=[trader, 'VIXY', dayEnd, .8, 3, 30, 0.00], name='vixy5MRKTMKR')
    vixy6MRKTMKR = threading.Thread(target=marketMaker, args=[trader, 'VIXY', dayEnd, .8, 3, 30, 0.00], name='vixy6MRKTMKR')
    """
    
    # --Initiate threads--
    
    trv1MRKTMKR.start()
    time.sleep(8)
    trv2MRKTMKR.start()
    time.sleep(8)
    trv3MRKTMKR.start()
    time.sleep(8)
    trv4MRKTMKR.start()
    time.sleep(8)
    trv5MRKTMKR.start()
    time.sleep(8)
    trv6MRKTMKR.start()
    time.sleep(8)
    trv7MRKTMKR.start()
    time.sleep(8)
    trv8MRKTMKR.start()
    time.sleep(8)
    
    """
    ba1MRKTMKR.start()
    time.sleep(8)
    ba2MRKTMKR.start()
    time.sleep(8)
    ba3MRKTMKR.start()
    time.sleep(8)
    ba4MRKTMKR.start()
    time.sleep(8)
    ba5MRKTMKR.start()
    time.sleep(8)
    ba6MRKTMKR.start()
    """
    """
    spy1MRKTMKR.start()
    time.sleep(8)
    spy2MRKTMKR.start()
    time.sleep(8)
    spy3MRKTMKR.start()
    time.sleep(8)
    spy4MRKTMKR.start()
    time.sleep(8)
    spy5MRKTMKR.start()
    time.sleep(8)
    spy6MRKTMKR.start()
    """
    """
    ko1MRKTMKR.start()
    time.sleep(8)
    ko2MRKTMKR.start()
    time.sleep(8)
    ko3MRKTMKR.start()
    time.sleep(8)
    ko4MRKTMKR.start()
    time.sleep(8)
    ko5MRKTMKR.start()
    time.sleep(8)
    ko6MRKTMKR.start()
    """
    """
    csco1MRKTMKR.start()
    time.sleep(8)
    csco2MRKTMKR.start()
    time.sleep(8)
    csco3MRKTMKR.start()
    time.sleep(8)
    csco4MRKTMKR.start()
    time.sleep(8)
    csco5MRKTMKR.start()
    time.sleep(8)
    csco6MRKTMKR.start()
    """
    """
    vixy1MRKTMKR.start()
    time.sleep(8)
    vixy2MRKTMKR.start()
    time.sleep(8)
    vixy3MRKTMKR.start()
    time.sleep(8)
    vixy4MRKTMKR.start()
    time.sleep(8)
    vixy5MRKTMKR.start()
    time.sleep(8)
    vixy6MRKTMKR.start()
    """

    # --Execute functions on threads-- 
    
    trv1MRKTMKR.join()
    trv2MRKTMKR.join()
    trv3MRKTMKR.join()
    trv4MRKTMKR.join()
    trv5MRKTMKR.join()
    trv6MRKTMKR.join()
    trv7MRKTMKR.join()
    trv8MRKTMKR.join()
    
    """
    ba1MRKTMKR.join()
    ba2MRKTMKR.join()
    ba3MRKTMKR.join()
    ba4MRKTMKR.join()
    ba5MRKTMKR.join()
    ba6MRKTMKR.join()
    """
    """
    spy1MRKTMKR.join()
    spy2MRKTMKR.join()
    spy3MRKTMKR.join()
    spy4MRKTMKR.join()
    spy5MRKTMKR.join()
    spy6MRKTMKR.join()
    """
    """
    ko1MRKTMKR.join()
    ko2MRKTMKR.join()
    ko3MRKTMKR.join()
    ko4MRKTMKR.join()
    ko5MRKTMKR.join()
    ko6MRKTMKR.join()
    """
    """
    csco1MRKTMKR.join()
    csco2MRKTMKR.join()
    csco3MRKTMKR.join()
    csco4MRKTMKR.join()
    csco5MRKTMKR.join()
    csco6MRKTMKR.join()
    """
    """
    vixy1MRKTMKR.join()
    vixy2MRKTMKR.join()
    vixy3MRKTMKR.join()
    vixy4MRKTMKR.join()
    vixy5MRKTMKR.join()
    vixy6MRKTMKR.join()
    """


    # Disconnect
    time.sleep(59) # Wait for all threads to sell inventory
    print("Final buying power:",trader.get_portfolio_summary().get_total_bp())
    trader.disconnect()

    return

if __name__ == "__main__":
    main(sys.argv)
