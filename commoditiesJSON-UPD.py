import yfinance as yf
import json
import os

# File name
json_file = 'assets/commodities.json'

# List of commodity tickers and names
commodities = {
    "CL=F": "Crude Oil",
    "BZ=F": "Brent Crude Oil",
    "HO=F": "Heating Oil",
    "NG=F": "Natural Gas",
    "GC=F": "Gold",
    "SI=F": "Silver",
    "PL=F": "Platinum",
    "PA=F": "Palladium",
    "HG=F": "Copper",
    "ZS=F": "Soybeans",
    "ZC=F": "Corn",
    "CC=F": "Cocoa",
    "KC=F": "Coffee",
    "CT=F": "Cotton",
    "RB=F": "RBOB Gasoline",
    "LBR=F": "Lumber"
}

# Load existing data from the JSON file if it exists
if os.path.exists(json_file):
    with open(json_file, 'r') as f:
        existing_data = json.load(f)
else:
    existing_data = []

# Convert the existing data into a dictionary of tickers for easy lookup
existing_data_dict = {commodity['Ticker']: commodity for commodity in existing_data}

# Dictionary to store new commodities data
new_data_dict = {}

# Iterate over the commodity tickers and add to the new data dictionary
for ticker, name in commodities.items():
    # Add to the new dictionary
    new_data_dict[ticker] = {
        "Name": name,
        "Ticker": ticker
    }

# Detect commodities that are no longer in the list
removed_commodities = [ticker for ticker in existing_data_dict if ticker not in new_data_dict]

# Update the JSON data
updated_data = list(new_data_dict.values())

# Save the updated data to the JSON file
with open(json_file, 'w') as f:
    json.dump(updated_data, f, indent=4)

print(f"Updated {json_file} with {len(new_data_dict)} commodities.")
print(f"Removed {len(removed_commodities)} commodities: {removed_commodities}")
