import sys
import time
import credentials
import datetime as dt
import shift


def trafficLight(rightNow, dayStart, wait):

    if dayStart > rightNow:
        print("Wait till market open")
        time.sleep(wait)
        print(dt.datetime.now())
        trafficLight(dt.datetime.now(), dayStart, wait)
    else:
        print("Begin Trading")
        return


def closePositions():

    # Cancel pending orders
    print("Waiting list size: " + str(trader.get_waiting_list_size()))
    print("Canceling all pending orders...")
    trader.cancel_all_pending_orders()
    print("Waiting list size: " + str(trader.get_waiting_list_size()))
    print("All pending orders cancelled") # Cancel outstanding open orders before entering closing orders

    # Close / Cover all open positions!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!TODO******************************************
    """
    either sell at market or at best bid w/ volume required
    """
    print("All closing orders submitted")

    return


def moneyMaker(dayEnd, lag):

    # Datetime beginning trading
    rightNow = dt.datetime.now()

    while(dayEnd > rightNow):
        print("Make trades ...",rightNow)
        time.sleep(lag)
        """
        make trades here
        """
        rightNow = dt.datetime.now() # Reset time rightNow

    # 90 seconds till end of trading day
    closePositions()

    # Done trading
    return


def main(argv):

    # Create trader object
    trader = shift.Trader(credentials.user) # Change to competition user!!!!!!!!!!!!!!!!!!!!!!!!!!!!CHANGE**********************

    # Connect and subscribe to all available order books
    try:
        trader.connect("initiator.cfg", credentials.password) # Change to competition pass!!!!!!!!!!!!!!!!!!!!!!!!!!!!CHANGE*************************
        trader.sub_all_order_book() # Subscribe to orderbook for all tickers.  cna also choose one particular stock
    except shift.IncorrectPasswordError as e:
        print(e)
    except shift.ConnectionTimeoutError as e:
        print(e)

    # Today's date
    today = dt.date.today()

    # Datetime right now
    rightNow = dt.datetime.now()

    # Start of trading day datetime
    #startTime = dt.time(10,30,00)!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!UNCOMMENT*************************
    startTime = dt.time(23,49,30)#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!REMOVE**************************
    dayStart = dt.datetime.combine(today,startTime)

    # Wait to begin trading
    trafficLight(rightNow, dayStart, 0.5)

    # End of trading day datetime
    #endTime = dt.time(16,58,30)!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!UNCOMMENT*************************
    endTime = dt.time(23,51,00)#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!REMOVE**************************
    dayEnd = dt.datetime.combine(today,endTime)

    # Begin trading
    moneyMaker(dayEnd, 0.25)
    
    # Disconnect
    trader.disconnect()

    return


if __name__ == "__main__":
    main(sys.argv)
