"""Manages the portfolio and liquidity files."""

import yfinance as yf
import json
import time
from manage_assets import check_cuantity, get_latest_price, load_portfolio_json, check_price
from manage_liquidity import check_liquidity_available, load_liquidity_json, save_liquidity_data, pair, calculate_total_liquidity


CURRENCIES = ["EUR", "USD", "GBP", "JPY", "CHF", "CNH"]
PORTFOLIO_FILE_PATH = 'assets/portfolio.json'


def save_portfolio_data(portfolio_data):
    """Saves liquidity data back to the JSON file."""
    try:
        with open(PORTFOLIO_FILE_PATH, 'w') as file:
            json.dump(portfolio_data, file, indent=4)
    except IOError:
        print(f"Error writing to {portfolio_file}.")
        


def execute_operation(ticker, cuantity, total_value, currency):
    """
    Updates the portfolio and liquidity files after a sale.

    Args:
        ticker (str): The symbol of the asset being sold.
        cuantity_to_sell (int): The quantity of the asset to be sold.
        total_value (float): The total value of the sale to update liquidity.
        currency (str): The currency in which the sale was made.
    """

    portfolio = load_portfolio_json()

    liquidity = load_liquidity_json()

    # Update the quantity in the portfolio
    if ticker in portfolio:
        portfolio[ticker] += cuantity  # Si existe, añade la cantidad
    else:
        portfolio[ticker] = cuantity  # Si no existe, inicializa con la cantidad
    liquidity[f"LIQ-{currency}"] += total_value

    # Save the updated portfolio
    save_portfolio_data(portfolio)

    # Save the updated liquidity
    save_liquidity_data(liquidity)



def sell_item(item_name, ticker):
    """Sell an item in your portfolio."""

    cuantity_item = check_cuantity(ticker)

    if cuantity_item == 0:
        print(f"You don't have {item_name} in your portfolio")
        return

    cuantity_to_sell = None
    while cuantity_to_sell is None:
        try:
            cuantity_to_sell = int(input(f"How much {item_name} you want to sell? "))
            if cuantity_to_sell > cuantity_item:
                print(f"You've got {cuantity_item} units, you don't have enough to sell {cuantity_to_sell} units.")
                cuantity_to_sell = None
        except ValueError:
            print("Enter a valid cuantity")

    currency = None
    while currency not in CURRENCIES:
        currency = input(f"In which currency you want to sell {item_name}? (EUR, USD, GBP, JPY, CHF, CNH). Type 'e' to exit: ").upper()
        if currency == 'e':
            return
    
    # Check market price for the ticker in the specified currency
    price_per_unit = check_price(ticker, currency)
    if price_per_unit is None:
        print(f"Error retrieving price for {item_name} in {currency}.")
        return

    # Calculate the total value of the sale
    total_value = price_per_unit * cuantity_to_sell

    # Process the sale
    confirm = input(f"You're selling {cuantity_to_sell} units of {item_name} at {price_per_unit} {currency} per unit. Total: {total_value} {currency}. Confirm (y/n)? ").lower()
    if confirm == 'y':
        execute_operation(ticker, -cuantity_to_sell, total_value, currency)
        print(f"Successfully sold {cuantity_to_sell} units of {item_name} for {total_value} {currency}.")
    else:
        print("Sale cancelled.")


def buy_item(item_name, ticker):
    
    """
    Interactively asks the user for a currency to buy an item in.
    
    Args:
        item_name (str): The name of the item to buy.
        ticker (str): The ticker symbol of the item to buy.
    """
    currency = None
    while currency not in CURRENCIES:
        currency = input(f"In which currency do you want to buy {item_name}? (EUR, USD, GBP, JPY, CHF, CNH). Type 'e' to exit: ").upper()
        if currency == 'e':
            return

    liquidity = check_liquidity_available(currency)

    if liquidity == 0:
        print(f"You can't purchase using {currency}, currently you've got 0.")
        return

    current_item_price = check_price(ticker, currency)

    max_amount = liquidity / current_item_price

    print(f"You can buy up to {max_amount} units of {ticker} using {liquidity} {currency}")

    amount_to_buy = None
    while amount_to_buy != 'e':
        user_input = input(f"You can buy up to {max_amount} units. Select a valid amount or type 'e': ")

        if user_input == 'e':
            print("Cancelling operation...")
            time.sleep(1)  # Asumiendo que has importado time
            return

        try:
            amount_to_buy = int(user_input)
            
            # Comprobar si amount_to_buy es válido
            if amount_to_buy <= 0:
                print("Please enter a positive number.")
            elif amount_to_buy > max_amount:
                print(f"You cannot buy {amount_to_buy} units. You can only buy up to {max_amount} units.")
            else:
                break  # Sale del bucle si la cantidad es válida
                
        except ValueError:
            print("Invalid input. Please enter a number or 'e' to exit.")

    
    total_value = current_item_price * amount_to_buy
    confirm = input(f"You're purchasing {amount_to_buy} units of {ticker} at {current_item_price} {currency} per unit. Total: {total_value} {currency}. Confirm (y/n)? ").lower()
    if confirm == 'y':
        execute_operation(ticker, amount_to_buy, -total_value, currency)
        print(f"Successfully bought {amount_to_buy} units of {item_name} for {total_value} {currency}.")
    else:
        print("Sale cancelled.")   
    
    

def update_asset(item_name, ticker):

    buy_or_sell = input(f"Do you want to buy or sell {item_name}? (b/s)").lower()

    if buy_or_sell == 'b':
        buy_item(item_name, ticker)
    elif buy_or_sell == 's':
        sell_item(item_name, ticker)

def calculate_total_value():

    total_value = 0
    portfolio = load_portfolio_json()

    for ticker, cuantity in portfolio.items():
        price = check_price(ticker, 'USD')

        if price is None:
            print(f"Error retrieving price for {ticker}.")
            continue

        total_value += cuantity * price

    total_value = round(total_value, 2)
    print(f"Your total value of your assets is {total_value} USD.")

    total_liquidity = calculate_total_liquidity()
    print(f"Your total liquidity is {total_liquidity} USD.")

    total_value += total_liquidity

    total_value = round(total_value, 2)
    print(f"Your net worth is {total_value} USD.")
    return total_value