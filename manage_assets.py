import yfinance as yf
import json
from manage_liquidity import pair

PORTFOLIO_FILE_PATH = 'assets/portfolio.json'

def load_portfolio_json() -> dict:
    """Loads the portfolio data from the JSON file."""
    try: 
        with open(PORTFOLIO_FILE_PATH, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: {PORTFOLIO_FILE_PATH} not found.")
        return 0
    except json.JSONDecodeError:
        print(f"Error: {PORTFOLIO_FILE_PATH} is not properly formatted.")
        return 0

def get_latest_price(ticker):
    """Fetch the latest price for a given ticker from Yahoo Finance."""
    try:
        asset = yf.Ticker(ticker)
        return round(asset.history(period="1d")['Close'].iloc[-1], 2)  # Get the last closing price  
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

def check_cuantity(ticker, asset_type):
    """Returns the amount of a given ticker in the portfolio, or 0 if not found."""
    try:
        return load_portfolio_json()[asset_type][ticker]
    except Exception as e:
        print(f"Ticker '{ticker}' is not in your portfolio.")
        return 0


def check_price(ticker, currency):
    """
    Fetches the current price of an asset (ticker) in the selected currency using yfinance 
    and the provided pair function for currency conversion.

    Args:
        ticker (str): The symbol of the asset whose price is to be obtained.
        currency (str): The currency in which to get the price.

    Returns:
        float: The price per unit of the asset in the specified currency.
        None: If the price for the asset or the currency cannot be obtained.
    """
    
    # Download the ticker data using yfinance
    asset_price = get_latest_price(ticker)

    # If the ticker does not have a price available
    if asset_price is None:
        print(f"Price for {ticker} not found.")
        return None

    # Convert to the desired currency using the pair function if it is not USD
    if currency != 'USD':
        try:
            conversion_rate = pair('USD', currency)  
            asset_price_converted = asset_price * conversion_rate
        except Exception as e:
            print(f"Error converting to {currency}: {e}")
            return None
    else:
        asset_price_converted = asset_price

    return round(asset_price_converted, 2)  # Return the price rounded to 2 decimal places


