import yfinance as yf
from fetch_item import search_component


action = input("""Which action you want to do:
                    \tUpdate a component (c)
                    \tCheck value of portfolio (v)
                    \tCheck risk of my portfolio (r)""")

if action == 'c':
    component = None
    print("Enter the name of the component (commodity, crypto or shares): ")
    while component != "exit" and component != "e" and component != 'q':
        component = input().lower()
        if component == "commodity":
            search_component('components\commodities.json')
        elif component == "crypto":
            search_component('components\crypto.json')
        elif component == "shares":
            search_component('components\shares.json')
        else:
            print("Type commodity, crypto or shares. If you want to exit type exit, e or q")
