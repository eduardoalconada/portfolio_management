import json
import os
from rapidfuzz import process, fuzz


# Load shares data from the JSON file
def load_data(asset_json):
    if os.path.exists(asset_json):
        with open(asset_json, 'r') as f:
            return json.load(f)
    else:
        print(f"Error: {asset_json} not found.")
        return []

# Function to find the closest matching company name or ticker
def find_item_or_ticker(query, asset_data):
    query_lower = query.strip().lower()
    
    # Step 1: Check for an exact ticker match
    for entry in asset_data:
        if entry["Ticker"].lower() == query_lower:
            return entry["Name"], entry["Ticker"]

    # Step 2: Fuzzy matching for item name
    item_names = [entry["Name"] for entry in asset_data]
    closest_match = process.extractOne(query, item_names, scorer=fuzz.WRatio)
    
    if closest_match:
        matched_name = closest_match[0]
        match_score = closest_match[1]

        # Return if the match score is reasonably high (say 60 or more)
        if match_score >= 60:
            for entry in asset_data:
                if entry["Name"].lower() == matched_name.lower():
                    return entry["Name"], entry["Ticker"]
        else:
            print(f"No good match found for '{query}'")
            return None, None
    else:
        print(f"No match found for '{query}'")
        return None, None

# Main function to interact with the user
def search_asset(asset_json):
    # Load the shares data
    asset_data = load_data(asset_json)
    
    # Ask the user for the company name or ticker input
    query = input("Enter the item name or ticker: ").strip()

    # Find the ticker or company name
    item_name, ticker = find_item_or_ticker(query, asset_data)

    # Output the result
    if item_name and ticker:
        print(f"The item is: {item_name}, Ticker: {ticker}")
    else:
        print("Could not find a matching item or ticker.")
    
    return item_name, ticker

# Run the program
if __name__ == "__main__":
    search_asset('assets/shares.json')
    search_asset('assets/commodities.json')
