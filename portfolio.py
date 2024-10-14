import yfinance as yf
from manage_portfolio import update_asset, calculate_total_value
from manage_liquidity import update_liquidity
from fetch_item import search_asset



action = None
while action != 'e':
    action = input("""Which action you want to do:
                        \tUpdate an asset (c)   
                        \tUpdate liquidity (l)
                        \tCheck value of portfolio (v)
                        \tCheck risk of my portfolio (r)
                        \tExit (e)\n""").lower()

    if action == 'c':
        asset = None
        print("Enter the name of the asset (commodity, crypto or shares): ")
        while asset != "exit" and asset != "e" and asset != 'q':
            asset = input().lower()
            if asset == "commodity":
                item_name, ticker = search_asset('assets\commodities.json')
                update_asset(item_name, ticker)
            elif asset == "crypto":
                item_name, ticker = search_asset('assets\crypto.json')
                update_asset(item_name, ticker)
            elif asset == "shares":
                item_name, ticker = search_asset('assets\shares.json')
                update_asset(item_name, ticker)
            else:
                print("Type commodity, crypto or shares. If you want to exit type 'exit', 'e' or 'q'")

    elif action == 'l':
        update_liquidity()
    
    elif action == 'v':
        calculate_total_value()
    
    elif action == 'r':
        print("Not implemented yet") 
    
    