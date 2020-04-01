import datetime as dt
import time


def trafficLight(rightNow, dayStart, wait):

    if dayStart > rightNow:
        print("Wait till market open")
        time.sleep(wait)
        print(rightNow)
        trafficLight(rightNow, dayStart, wait)
    else:
        print("Begin Trading")
        return