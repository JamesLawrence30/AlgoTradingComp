import shift

def manageInventory(trader: shift.Trader, ticker):

    item = trader.get_portfolio_item(ticker)
    numShares = int(item.get_shares() / 100) # Order size in 100's of shares, strictly as an int
    print("On hand:", numShares)
    tradedPrice = item.get_price()
    unrealizedPL = 0

    if numShares > 0:
        unrealizedPL = ((trader.get_close_price("AAPL", False, numShares) - tradedPrice)/tradedPrice)*100

    elif numShares < 0:
        unrealizedPL = ((trader.get_close_price("AAPL", True, -numShares) - tradedPrice)/tradedPrice)*100

    if unrealizedPL >= 3.0: # Target met, take profit
        if item.get_shares() > 0:
            closeLong = shift.Order(shift.Order.Type.MARKET_SELL, item.get_symbol(), numShares)
            trader.submit_order(closeLong)
            print(ticker, "take profit on long")
        elif item.get_shares() < 0:
            coverShort = shift.Order(shift.Order.Type.MARKET_BUY, item.get_symbol(), -numShares)
            trader.submit_order(coverShort)
            print(ticker, "take profi on short")

    elif unrealizedPL <= -0.5: # Stop loss met, sell risk
        if item.get_shares() > 0:
            closeLong = shift.Order(shift.Order.Type.MARKET_SELL, item.get_symbol(), numShares)
            trader.submit_order(closeLong)
            print(ticker, "stop loss on long")
        elif item.get_shares() < 0:
            coverShort = shift.Order(shift.Order.Type.MARKET_BUY, item.get_symbol(), -numShares)
            trader.submit_order(coverShort)
            print(ticker, "stop loss on short")

    print("Remaining:", numShares)