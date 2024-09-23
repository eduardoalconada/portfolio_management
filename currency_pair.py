import yfinance as yf

def pair(base, quote):
    try:
        # Fetch the currency pair data from Yahoo Finance
        a_to_b = yf.Ticker(f"{base}{quote}=X")
        
        # Get the latest exchange rate (closing price for the last day)
        data = a_to_b.history(period="1d")

        # Check if data is empty
        if data.empty:
            print(f"No data available for {base}/{quote}.")
            return None

        # Safely retrieve the last closing price
        a_to_b_rate = data['Close'].iloc[-1]
        
        # Return the exchange rate
        return a_to_b_rate

    except IndexError:
        print(f"Error: Unable to retrieve the latest closing price for {base}/{quote}. Data may be unavailable.")
        return None
    except Exception as e:
        print(f"An error occurred while fetching data for {base}/{quote}: {e}")
        return None

