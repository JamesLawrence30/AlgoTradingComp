import shift

def checkInventory(trader: shift.Trader, ticker):
    item = trader.get_portfolio_item(ticker)
    midprice = (trader.get_best_price(ticker).get_bid_price()+trader.get_best_price(ticker).get_ask_price())/2
    if item.get_price() >= midprice: # If we can break even or take any profit, sell
        for order in trader.get_waiting_list():
            if order.symbol == ticker and order.Type == 'Type.LIMIT_SELL': # Cancel unfilled limit sells so we can dump them at market
                trader.submit_cancellation(order)
        #sellSize = max(0,min(item.get_shares(), trader.get_best_price(ticker).get_ask_size())) # Sell up to the amount asked for, don't try to sell more than we have. Also no shorts
        sellSize = 1
        sellRisk = shift.Order(shift.Order.Type.MARKET_SELL, ticker, sellSize) # Sell inventory to reduce risk
        trader.submit_order(sellRisk)
        print("Sold off", sellSize, ticker)