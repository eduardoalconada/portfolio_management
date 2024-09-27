import json
import os
from rapidfuzz import process, fuzz

# File name for shares data
json_file = 'components/shares.json'

# Load shares data from the JSON file
def load_shares():
    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            return json.load(f)
    else:
        print(f"Error: {json_file} not found.")
        return []

# Function to find the closest matching company name or ticker
def find_company_or_ticker(query, shares_data):
    query_lower = query.strip().lower()
    
    # Step 1: Check for an exact ticker match
    for entry in shares_data:
        if entry["Ticker"].lower() == query_lower:
            return entry["Name"], entry["Ticker"]

    # Step 2: Fuzzy matching for company name
    company_names = [entry["Name"] for entry in shares_data]
    closest_match = process.extractOne(query, company_names, scorer=fuzz.WRatio)
    
    if closest_match:
        matched_name = closest_match[0]
        match_score = closest_match[1]

        # Return if the match score is reasonably high (say 60 or more)
        if match_score >= 60:
            for entry in shares_data:
                if entry["Name"].lower() == matched_name.lower():
                    return entry["Name"], entry["Ticker"]
        else:
            print(f"No good match found for '{query}'")
            return None, None
    else:
        print(f"No match found for '{query}'")
        return None, None

# Main function to interact with the user
def main():
    # Load the shares data
    shares_data = load_shares()
    
    # Ask the user for the company name or ticker input
    query = input("Enter the company name or ticker: ").strip()

    # Find the ticker or company name
    company_name, ticker = find_company_or_ticker(query, shares_data)

    # Output the result
    if company_name and ticker:
        print(f"The company is: {company_name}, Ticker: {ticker}")
    else:
        print("Could not find a matching company or ticker.")

# Run the program
if __name__ == "__main__":
    main()
