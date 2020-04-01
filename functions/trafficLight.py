import datetime as dt
import time
import shift


def trafficLight(trader: shift.Trader, dayStart, wait):
    
    rightNow = trader.get_last_trade_time()
    if dayStart > rightNow:
        print("Wait till market open")
        time.sleep(wait)
        print(rightNow)
        trafficLight(trader, dayStart, wait)
    else:
        print("Begin Trading")
        return