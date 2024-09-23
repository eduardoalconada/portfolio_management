import yfinance as yf
import json
from calcEUR2USD import pairUSD2EUR

with open('components/commodities.json', 'r') as f:
    data = json.load(f)

for metal in data:
    data_metal_ = yf.Ticker(data[metal][0])
    price_usd = data_metal_.history(period='1d').iloc[-1]['Close']
    price_eur = price_usd*pairUSD2EUR()
    data[metal][1] = round(price_eur,2)
    
with open('components/commodities.json', 'w') as f:
    json.dump(data, f, indent=4)