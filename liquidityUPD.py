import yfinance as yf
import json

# Constants for currencies
CURRENCIES = ["EUR", "USD", "GBP", "JPY", "CHF", "CNH"]
LIQUIDITY_FILE_PATH = 'components/liquidity.json'

def open_liq_json():
    """Open the liquidity JSON file and load data."""
    try:
        with open(LIQUIDITY_FILE_PATH, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {f"LIQ-{currency}": 0 for currency in CURRENCIES}
    return data

def write_data(file, data):
    """Write liquidity data to the JSON file."""
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

def display_currency_options():
    """Display available currency options to the user."""
    print("\n".join([f"\t{i + 1}. {currency} (type {currency})" for i, currency in enumerate(CURRENCIES)]))

def transfer_liquidity(data):
    """Transfer liquidity between currencies."""
    transfer = input("Do you want to transfer from a currency to another? (y/n) ").lower()
    if transfer == 'y':
        display_currency_options()
        base = input("Which currency will be the base? ").upper()
        quote = input("Which currency will be the quote? ").upper()
        
        if base not in CURRENCIES or quote not in CURRENCIES:
            print("Invalid currency selection. Please try again.")
            return data
        
        base_amount = int(input("Enter the amount you want to exchange: "))
        
        if base_amount > data[f"LIQ-{base}"]:
            print(f"You do not have enough liquidity of {base}.")
        else:
            quote_amount = base_amount * pair(base, quote)
            data[f"LIQ-{base}"] -= base_amount
            data[f"LIQ-{quote}"] += quote_amount
            print(f"Transferred {base_amount} {base} to {quote_amount} {quote}.")
    
    return data

def update_amount(data): 
    """Update the amount of liquidity for a specific currency."""
    upd_amount = input("Do you want to update the amount of liquidity? (y/n) ").lower()

    if upd_amount == "y":
        display_currency_options()
        currency = input("Which currency do you want to update? ").upper()
        
        if currency not in CURRENCIES:
            print("Invalid currency selection. Please try again.")
            return data
        
        red_inc = input("Do you want to increase or reduce the amount? (i/r) ").lower()
        
        if red_inc not in ['i', 'r']:
            print("Invalid option selected. Please try again.")
            return data
        
        amount = int(input("Enter the amount: "))
        
        if red_inc == 'i':
            data[f"LIQ-{currency}"] += amount
        elif red_inc == 'r':
            if amount > data[f"LIQ-{currency}"]:
                print(f"You do not have enough liquidity of {currency}.")
            else:
                data[f"LIQ-{currency}"] -= amount

    return data

if __name__ == "__main__":
    data = open_liq_json()

    data_amount_updated = update_amount(data)

    data_transfered = transfer_liquidity(data_amount_updated)
    
    write_data(LIQUIDITY_FILE_PATH, data_transfered)
