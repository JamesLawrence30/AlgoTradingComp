import shift
import time

from closePositions import closePositions

def manageInventory(trader: shift.Trader, ticker, dayEnd):

    # Datetime of simulation
    rightNow =  trader.get_last_trade_time()

    # While the time is before end of day...
    while(dayEnd > rightNow):

        time.sleep(5) # Give prices time to fluctuate

        item = trader.get_portfolio_item(ticker)
        if item.get_shares() != 0:
            
            unrealizedPL = 0
            tradedPrice = item.get_price()
            numShares = int(item.get_shares() / 100) # Order size in 100's of shares, strictly as an int

            if numShares > 0:
                unrealizedPL = ((trader.get_close_price(ticker, False, numShares) - tradedPrice)/tradedPrice)*100

            else:# numShares < 0:
                unrealizedPL = -((trader.get_close_price(ticker, True, -numShares) - tradedPrice)/tradedPrice)*100

            print(ticker, "Unrealized P/L:", unrealizedPL,"%")
            if unrealizedPL >= 0.40: # Target met, take profit
                #if unrealizedPL >= 3.0: # Target met, take profit
                if item.get_shares() > 0:
                    closePositions(trader, ticker)
                    """
                    closeLong = shift.Order(shift.Order.Type.MARKET_SELL, item.get_symbol(), numShares)
                    trader.submit_order(closeLong)
                    """
                    print(ticker, "take profit on long")
                    time.sleep(5) # Don't act on volatile spikes and dips, only identify longer trends
                elif item.get_shares() < 0:
                    closePositions(trader, ticker)
                    """
                    coverShort = shift.Order(shift.Order.Type.MARKET_BUY, item.get_symbol(), -numShares)
                    trader.submit_order(coverShort)
                    """
                    print(ticker, "take profit on short")
                    time.sleep(5) # Don't act on volatile spikes and dips, only identify longer trends

            elif unrealizedPL <= -0.30: # Stop loss met, sell risk
                #elif unrealizedPL <= -0.50: # Stop loss met, sell risk
                if item.get_shares() > 0:
                    closePositions(trader, ticker)
                    """
                    closeLong = shift.Order(shift.Order.Type.MARKET_SELL, item.get_symbol(), numShares)
                    trader.submit_order(closeLong)
                    """
                    print(ticker, "stop loss on long")
                    time.sleep(5) # Don't act on volatile spikes and dips, only identify longer trends
                elif item.get_shares() < 0:
                    closePositions(trader, ticker)
                    """
                    coverShort = shift.Order(shift.Order.Type.MARKET_BUY, item.get_symbol(), -numShares)
                    trader.submit_order(coverShort)
                    """
                    print(ticker, "stop loss on short")
                    time.sleep(5) # Don't act on volatile spikes and dips, only identify longer trends


        rightNow =  trader.get_last_trade_time() # Reset datetime of right now