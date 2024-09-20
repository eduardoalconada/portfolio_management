import yfinance as yf
import json
import time
import requests
from calcEUR2USD import pairEUR2USD

def update_liquidity(liq_eur):

    liq_usd = liq_eur * pairEUR2USD()

    data["LIQ-USD"] = liq_usd

    with open('components/liquidity.json', 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":

    try:
        with open('components/liquidity.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"LIQ-EUR": 0, "LIQ-USD": 0}



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


    update_liquidity(data["LIQ-EUR"])
