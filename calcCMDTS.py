import yfinance as yf
import json




def create_dict():

    with open('components/commodities.json', 'r') as f:
        data_cmdt = json.load(f)
    
    with open('components/shares.json', 'r') as f:
        data_shares = json.load(f)

    final_dict = {}
    price = None
    for item in data_cmdt:
        if item["Num stocks"] > 0:
            try:
                # Use yfinance to fetch the ticker data
                ticker_data = yf.Ticker(item["Ticker"])
                
                # Get the latest price (from the last available market data)
                todays_data = ticker_data.history(period='1d')
                
                if not todays_data.empty:
                    # Return the closing price of the latest available trading day
                    price = todays_data['Close'][0]
                    final_dict[item["Name"]] = price*item["Num stocks"]
                else:
                    print(f"No data available for ticker: {ticker}")
                    pass
            except Exception as e:
                print(f"Error fetching price for ticker {ticker}: {e}")
                pass
    print(final_dict)
    return final_dict


create_dict()