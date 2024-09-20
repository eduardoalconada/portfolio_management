import yfinance as yf
import json
import requests
import os

def calculate_commodities_value(json_file_path):
    """
    Calculates the value in USD and EUR of the commodities in the specified JSON file.

    Args:
        json_file_path (str): The path to the JSON file.

    Returns:
        dict: Dictionary with the total value in USD and EUR.
    """

    # Get the EUR/USD exchange rate
    url = "https://api.exchangerate-api.com/v4/latest/EUR"
    response = requests.get(url)
    data = response.json()
    exchange_rate = data['rates']['USD']

    # Initialize total values
    total_value_usd = 0
    total_value_eur = 0

    # Load the JSON data
    with open(json_file_path, 'r') as f:
        cmdts_data = json.load(f)

    # Iterate over each commodity in the JSON
    for commodity, quantity in cmdts_data.items():
        # Get the current price of the commodity in USD (adjust the ticker as needed)
        ticker = commodity  # Assuming the ticker matches the label
        try:
            data = yf.download(tickers=ticker, period='1d', interval='1m')
            price_usd = data['Close'].iloc[-1]

            # Convert the price to EUR
            price_eur = price_usd / exchange_rate

            # Calculate the total value of the commodity
            value_usd = quantity * price_usd
            value_eur = quantity * price_eur

            total_value_usd += value_usd
            total_value_eur += value_eur

            print(f"Commodity: {commodity}, Quantity: {quantity}, Value in USD: {value_usd}, Value in EUR: {value_eur}")
        except Exception as e:
            print(f"Error getting price for {commodity}: {e}")

    return {"total_value_usd": total_value_usd, "total_value_eur": total_value_eur}

# Assuming the JSON file is in a 'components' folder
json_file = "components/commodities.json"
result = calculate_commodities_value(json_file)
print("Total value in USD:", result["total_value_usd"])
print("Total value in EUR:", result["total_value_eur"])