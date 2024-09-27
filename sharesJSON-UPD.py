import pandas as pd
import json
import os

# File name
json_file = 'components/shares.json'

def shares_upd():

    # Load existing data from the JSON file if it exists
    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    # Convert the existing data into a set of tickers for easy lookup
    existing_tickers = {company['Ticker'] for company in existing_data}

    # Fetch S&P 500 stock data from Wikipedia
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    tables = pd.read_html(url)

    # The first table on the page contains the S&P 500 companies
    sp500_table = tables[0]

    # List to store new companies' data
    new_companies = []

    # Iterate over the S&P 500 table rows
    for _, row in sp500_table.iterrows():
        ticker = row['Symbol']
        company_name = row['Security']
        
        if ticker not in existing_tickers:
            company_data = {
                "Name": company_name,       # Company name
                "Ticker": ticker            # Stock ticker symbol
            }
            new_companies.append(company_data)

    # Combine old and new companies
    all_companies = existing_data + new_companies

    # Save the updated data to the JSON file
    with open(json_file, 'w') as f:
        json.dump(all_companies, f, indent=4)

    print(f"Data updated in {json_file}")

if __name__ == "__main__":
    shares_upd()