import yfinance as yf
from manage_portfolio import update_asset
from manage_liquidity import update_liquidity
from fetch_item import search_asset


action = input("""Which action you want to do:
                    \tUpdate liquidity (l)
                    \tUpdate a component (c)
                    \tCheck value of portfolio (v)
                    \tCheck risk of my portfolio (r)\n""")

if action == 'c':
    component = None
    print("Enter the name of the component (commodity, crypto or shares): ")
    while component != "exit" and component != "e" and component != 'q':
        component = input().lower()
        if component == "commodity":
            item_name, ticker = search_asset('components\commodities.json')
            update_asset(item_name, ticker)
        elif component == "crypto":
            item_name, ticker = search_asset('components\crypto.json')
            update_asset(item_name, ticker)
        elif component == "shares":
            item_name, ticker = search_asset('components\shares.json')
            update_asset(item_name, ticker)
        else:
            print("Type commodity, crypto or shares. If you want to exit type 'exit', 'e' or 'q'")

if action == 'l':
    update_liquidity()