import shift

def manageInventory(trader: shift.Trader, ticker):

    #item = trader.get_portfolio_item(ticker) #!!!!!!!!!!!!needs to look at open orders not inventory
    
    if item.get_realized_pl() >= 3.0: # Target met, take profit
        if item.get_shares() > 0:
            closeLong = shift.Order(shift.Order.Type.MARKET_SELL, item.get_symbol(), int(item.get_shares() / 100)) # Order size in 100's of shares, strictly as an int
            trader.submit_order(closeLong)
            print(ticker, "take profit on long")
        elif item.get_shares() < 0:
            coverShort = shift.Order(shift.Order.Type.MARKET_BUY, item.get_symbol(), int(item.get_shares() / -100))
            trader.submit_order(coverShort)
            print(ticker, "take profi on short")

    elif item.get_realized_pl() <= -0.5: # Stop loss met, sell risk
        if item.get_shares() > 0:
            closeLong = shift.Order(shift.Order.Type.MARKET_SELL, item.get_symbol(), int(item.get_shares() / 100)) # Order size in 100's of shares, strictly as an int
            trader.submit_order(closeLong)
            print(ticker, "stop loss on long")
        elif item.get_shares() < 0:
            coverShort = shift.Order(shift.Order.Type.MARKET_BUY, item.get_symbol(), int(item.get_shares() / -100))
            trader.submit_order(coverShort)
            print(ticker, "stop loss on short")