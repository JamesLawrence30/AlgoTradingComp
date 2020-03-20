import sys
import time
import credentials
import numpy as np
import datetime as dt
import shift

def portfolioSummary(trader: shift.Trader):
    print("Buying Power\tTotal Shares\tTotal P&L\tTimestamp")
    print(
        "%12.2f\t%12d\t%9.2f\t%26s"
        % (
            trader.get_portfolio_summary().get_total_bp(),
            trader.get_portfolio_summary().get_total_shares(),
            trader.get_portfolio_summary().get_total_realized_pl(),
            trader.get_portfolio_summary().get_timestamp(),
        )
    )

    print()

    print("Symbol\t\tShares\t\tPrice\t\t  P&L\tTimestamp")
    for item in trader.get_portfolio_items().values():
        print(
            "%6s\t\t%6d\t%9.2f\t%9.2f\t%26s"
            % (
                item.get_symbol(),
                item.get_shares(),
                item.get_price(),
                item.get_realized_pl(),
                item.get_timestamp(),
            )
        )

    print()

    return


def closePositions(trader: shift.Trader):

    # Cancel pending orders
    print("Waiting list size: " + str(trader.get_waiting_list_size()) + " , Canceling all pending orders...")
    for order in trader.get_waiting_list():
        trader.submit_cancellation(order)
    print("All pending orders cancelled") # Cancel outstanding open orders before entering closing orders


    # Close / Cover all open positions
    portfolioSummary(trader) # Print summary of portfolio
    for item in trader.get_portfolio_items().values():
        if item.get_shares() > 0:
            print("Open long positions")
            closeLong = shift.Order(shift.Order.Type.MARKET_SELL, item.get_symbol(), int(item.get_shares() / 100)) # Order size in 100's of shares, strictly as an int
            trader.submit_order(closeLong)
        if item.get_shares() < 0:
            print("Open short positions")
            coverShort = shift.Order(shift.Order.Type.MARKET_BUY, item.get_symbol(), int(item.get_shares() / -100))
            trader.submit_order(coverShort)
    print("All closing orders submitted")


    return


def firstStrategy(trader: shift.Trader, ticker, dayEnd, lag):

    # Datetime of simulation
    rightNow =  trader.get_last_trade_time()

    # FIFO queue initialized
    priceQueue = []

    signal = 'S'
    # While the time is before end of day...
    while(dayEnd > rightNow):
        # Pause and wait for change in prices
        time.sleep(lag)
        print(rightNow, "Total P/L:",trader.get_portfolio_summary().get_total_realized_pl())
        """
        Make Trades Here:
        """
        if len(priceQueue) > 2: # Queue is full
            firstDeriv = np.gradient(priceQueue, 1) # Find rate of change of prices

            # Prices switch from decreasing to increasing = buy  [buy @ local minima]
            if firstDeriv[2] > 0 and signal is 'S':
                #trader.cancel_all_pending_orders() # Make sure we have buying power
                limit_buy = shift.Order(shift.Order.Type.LIMIT_BUY, ticker, 10, trader.get_best_price(ticker).get_bid_price())
                trader.submit_order(limit_buy)
                print("buy @", trader.get_last_price(ticker))
                signal = 'B'
            # Prices switch from increasing to decreasing = sell  [sell @ local maxima]
            elif firstDeriv[2] < 0 and signal is 'B':
                #trader.cancel_all_pending_orders() # Make sure we have buying power
                limit_buy = shift.Order(shift.Order.Type.LIMIT_SELL, ticker, 10, trader.get_best_price(ticker).get_ask_price())
                trader.submit_order(limit_buy)
                print("sell @", trader.get_last_price(ticker))
                signal = 'S'

            # Drop oldest price, shift the prices over, add the newest price to queue
            priceQueue[0]=priceQueue[1]
            priceQueue[1]=priceQueue[2]
            priceQueue[2]=trader.get_last_price(ticker)

        else: # Queue is not full
            priceQueue.append(trader.get_last_price(ticker)) # Fill the queue from oldest price to latest price


        rightNow =  trader.get_last_trade_time() # Reset datetime of right now

    # 90 seconds till end of trading day
    closePositions(trader)

    # Done trading
    return


def marketMaker(trader: shift.Trader, ticker, dayEnd, lag):

    # Datetime of simulation
    rightNow =  trader.get_last_trade_time()

    count = 1
    # While the time is before end of day...
    while(dayEnd > rightNow):
        print(rightNow, "Total P/L:",trader.get_portfolio_summary().get_total_realized_pl())
        """
        Make Trades Here:
        """
        if count % ((1/lag)*10) == 0: # Every so often, sell off inventory.  Wait longer if lower lag
        	closePositions(trader)
        	print("Sold inventory, risk reset")

        time.sleep(lag) # Give prices some time to change

        # Submit a buy order
        limit_buy = shift.Order(shift.Order.Type.LIMIT_BUY, ticker, 1, trader.get_best_price(ticker).get_bid_price()) # Can buy +0.5 above bid with wide spread, or -.01 below if high volume
        trader.submit_order(limit_buy)
        print("Bought")

        time.sleep(0.1) # Allow a brief time for the order to fill

        # Sell if the buy order filled
        if trader.get_order(limit_buy.id).status == shift.Order.Status.FILLED:
        	limit_sell = shift.Order(shift.Order.Type.LIMIT_SELL, ticker, 1, trader.get_best_price(ticker).get_ask_price()) # Can sell -.05 below ask with wide spread, or +.01 above if high volume
        	trader.submit_order(limit_sell)
        	print("Filled buy and Sold")

        # Otherwise cancel the buy order
        else:
            for order in trader.get_waiting_list():
                trader.submit_cancellation(order)
            print("Cancelled")

        count = count + 1 # Increment counter
        rightNow =  trader.get_last_trade_time() # Reset datetime of right now

    # 60 seconds till end of trading day
    closePositions(trader)

    # Done trading
    return


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
    #endTime = dt.time(10,11,30) # **Set time for development**
    dayEnd = dt.datetime.combine(today,endTime)

    # Begin trading
    print("Initial buying power:",trader.get_portfolio_summary().get_total_bp())

    #ticker = "SPY"
    #firstStrategy(trader, ticker, dayEnd, 5.0)

    ticker = "SPY" # "BA"
    marketMaker(trader, ticker, dayEnd, .4)
    
    # Disconnect
    print("Final buying power:",trader.get_portfolio_summary().get_total_bp())
    trader.disconnect()

    return


if __name__ == "__main__":
    main(sys.argv)
