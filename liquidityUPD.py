import yfinance as yf
import json
import time
import requests
from calcEUR2USD import pairEUR2USD

path_liq = 'components/liquidity.json'

def update_liquidity(liq_eur):

    liq_usd = liq_eur * pairEUR2USD()

    data["LIQ-USD"] = round(liq_usd, 2)

    with open(path_liq, 'w') as f:
        json.dump(data, f, indent=4)

def open_liq_json():
    try:
        with open(path_liq, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"LIQ-EUR": 0, "LIQ-USD": 0}

    return data

def update_amount(data): 

    upd_amount = input("Do you want to update the amount of liquidity? (y/n)").lower()

    if upd_amount == "y":
        red_inc = input("Do you want to increase or reduce the amount? (i/r)").lower()
        amount = int(input("Enter the amount: "))
        if red_inc == 'i':
            data["LIQ-EUR"] += amount
        elif red_inc == 'r':
            data["LIQ-EUR"] -= amount
            
        with open('components/liquidity.json', 'w') as f:
            json.dump(data, f, indent=4)

if __name__ == "__main__":
    
    data = open_liq_json()

    update_amount(data)

    update_liquidity(data["LIQ-EUR"])
