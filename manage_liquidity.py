import yfinance as yf
import json

# Constants for currencies
CURRENCIES = ["EUR", "USD", "GBP", "JPY", "CHF", "CNH"]
LIQUIDITY_FILE_PATH = 'assets/liquidity.json'


def check_liquidity_available(currency):
    try:
        return load_liquidity_json()[f"LIQ-{currency}"]
    except Exception as e:
        print(f"You don't have {currency}.")


def pair(base, quote):
    """Fetches the exchange rate between two currencies."""
    try:
        # Fetch the currency pair data from Yahoo Finance
        ticker = yf.Ticker(f"{base}{quote}=X")
        data = ticker.history(period="1d")
        
        # If no data is available, return None
        if data.empty:
            print(f"No data available for {base}/{quote}.")
            return None
        
        # Return the latest closing price
        return data['Close'].iloc[-1]

    except IndexError:
        print(f"Error: Could not retrieve the latest price for {base}/{quote}.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def load_liquidity_json() -> dict:
    """Loads the liquidity data from the JSON file."""
    try:
        with open(LIQUIDITY_FILE_PATH, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        # Initialize the liquidity file if it doesn't exist
        return {f"LIQ-{currency}": 0 for currency in CURRENCIES}

def save_liquidity_data(liquidity_data):
    """Saves liquidity data back to the JSON file."""
    try:
        with open(LIQUIDITY_FILE_PATH, 'w') as file:
            json.dump(liquidity_data, file, indent=4)
    except IOError as e:
        print(f"Error writing to {LIQUIDITY_FILE_PATH}: {e}")

def display_currency_options():
    """Displays available currency options."""
    for i, currency in enumerate(CURRENCIES):
        print(f"\t{i + 1}. {currency} (type {currency})")

def prompt_transfer_liquidity(liquidity_data):
    """Prompts the user to transfer liquidity between currencies."""
    if input("Do you want to transfer from one currency to another? (y/n): ").lower() != 'y':
        return liquidity_data

    display_currency_options()
    base_currency = input("Which currency will be the base? ").upper()
    quote_currency = input("Which currency will be the quote? ").upper()

    if base_currency not in CURRENCIES or quote_currency not in CURRENCIES:
        print("Invalid currency selection.")
        return liquidity_data

    base_amount = int(input(f"Enter the amount of {base_currency} to exchange: "))

    if base_amount > liquidity_data[f"LIQ-{base_currency}"]:
        print(f"Insufficient {base_currency} liquidity.")
        return liquidity_data

    exchange_rate = pair(base_currency, quote_currency)
    if not exchange_rate:
        print("Failed to retrieve exchange rate.")
        return liquidity_data

    quote_amount = base_amount * exchange_rate
    liquidity_data[f"LIQ-{base_currency}"] -= base_amount
    liquidity_data[f"LIQ-{quote_currency}"] += quote_amount

    print(f"Transferred {base_amount} {base_currency} to {quote_amount:.2f} {quote_currency}.")
    return liquidity_data

def prompt_update_liquidity(liquidity_data):
    """Prompts the user to update liquidity for a specific currency."""
    if input("Do you want to update the amount of liquidity? (y/n): ").lower() != 'y':
        return liquidity_data

    display_currency_options()
    currency = input("Which currency do you want to update? ").upper()

    if currency not in CURRENCIES:
        print("Invalid currency selection.")
        return liquidity_data

    action = input("Increase or reduce the amount? (i/r): ").lower()
    if action not in ['i', 'r']:
        print("Invalid option selected.")
        return liquidity_data

    amount = int(input(f"Enter the amount to {('increase' if action == 'i' else 'reduce')}: "))

    if action == 'r' and amount > liquidity_data[f"LIQ-{currency}"]:
        print(f"Insufficient {currency} liquidity.")
        return liquidity_data

    liquidity_data[f"LIQ-{currency}"] += amount if action == 'i' else -amount
    return liquidity_data

def update_liquidity():
    """Main function to handle liquidity updates and transfers."""
    liquidity_data = load_liquidity_json()

    # Update liquidity amounts and transfer between currencies
    liquidity_data = prompt_update_liquidity(liquidity_data)
    liquidity_data = prompt_transfer_liquidity(liquidity_data)

    # Save the updated liquidity data
    save_liquidity_data(liquidity_data)
