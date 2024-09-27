import yfinance as yf


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
            upd_commodity()
        elif component == "crypto":
            upd_crypto()
        elif component == "shares":
            upd_shares()
        else:
            print("Type commodity, crypto or shares. If you want to exit type exit, e or q")
