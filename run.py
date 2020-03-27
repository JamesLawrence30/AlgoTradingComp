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

    time.sleep(.5)
    # Date of simulation
    today = trader.get_last_trade_time().date()

    # End of trading day datetime
    endTime = dt.time(16,59,0) # Competition time
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
    """
    cscoMRKTMKR = threading.Thread(target=marketMaker, args=[trader, 'CSCO', dayEnd, 3, 20, 0.00], name='cscoMRKTMKR')
    vixyMRKTMKR = threading.Thread(target=marketMaker, args=[trader, 'VIXY', dayEnd, 3, 20, 0.00], name='vixyMRKTMKR')
    """
    baMRKTMKR = threading.Thread(target=marketMaker, args=[trader, 'BA', dayEnd, 3, 20, -0.02], name='baMRKTMKR')
    spyMRKTMKR = threading.Thread(target=marketMaker, args=[trader, 'SPY', dayEnd, 3, 20, 0.00], name='spyMRKTMKR')
    trvMRKTMKR = threading.Thread(target=marketMaker, args=[trader, 'TRV', dayEnd, 3, 20, 0.01], name='trvMRKTMKR')
    #unhMRKTMKR = threading.Thread(target=marketMaker, args=[trader, 'UNH', dayEnd, 3, 20, 0.01], name='unhMRKTMKR')
    
    # Initiate threads
    """
    cscoMRKTMKR.start()
    vixyMRKTMKR.start()
    """
    baMRKTMKR.start()
    spyMRKTMKR.start()
    trvMRKTMKR.start()
    #unhMRKTMKR.start()

    # Execute functions on threads    
    """
    cscoMRKTMKR.join()
    vixyMRKTMKR.join()
    """
    baMRKTMKR.join()
    spyMRKTMKR.join()
    trvMRKTMKR.join()
    #unhMRKTMKR.join()


    # Disconnect
    print("Final buying power:",trader.get_portfolio_summary().get_total_bp())
    trader.disconnect()

    return

if __name__ == "__main__":
    main(sys.argv)
