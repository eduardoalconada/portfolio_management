import matplotlib.pyplot as plt
import plotly.graph_objs as go
from manage_assets import check_price
from manage_liquidity import pair


class Portfolio:
    def __init__(self, quote_currency, portfolio_json, liquidity_json):
        self.quote_currency = quote_currency
        self.portfolio_json = portfolio_json
        self.liquidity_json = liquidity_json
        self.commoditties, self.shares,self.crypto, self.liquidity, self.total_value = self.initialize()
    
    def initialize(self):
        commoditties = {"Total": 0}
        shares = {"Total": 0}
        crypto = {"Total": 0}
        liquidity = {"Total": 0}
        total_value = 0
        for asset_type, assets in self.portfolio_json.items():
            total_type = 0

            # Iterate over each item in the asset type
            for ticker, quantity in assets.items():
                price = check_price(ticker, self.quote_currency)

                if price is None:
                    print(f"Error retrieving price for {ticker}.")
                    continue

                # The total value of an item is calculated and summed to the total value of the asset type
                total_item = quantity * price
                
                if asset_type == "Commodities":
                    commoditties[ticker] = round(total_item, 2)
                    commoditties["Total"] += round(total_item, 2)
                elif asset_type == "Shares":
                    shares[ticker] = round(total_item, 2)
                    shares["Total"] += round(total_item, 2)
                elif asset_type == "Crypto":
                    crypto[ticker] = round(total_item, 2) 
                    crypto["Total"] += round(total_item, 2)
            total_value += round(total_type, 2)

        for currency, amount in self.liquidity_json.items():
            if not currency.startswith("LIQ-") or amount <= 0:
                continue

            pairity = pair(currency[4:], self.quote_currency)
            if pairity is None:
                continue

            total_currency = round(amount * pairity, 2)
            liquidity["Total"] += total_currency
            liquidity[currency] = total_currency

        # print(commoditties, shares, crypto, liquidity, total_value)
        return commoditties, shares, crypto, liquidity, total_value 
    
    def update_portfolio(self, portfolio_json_to_compare, liquidity_json_to_compare):
        if portfolio_json_to_compare != self.portfolio_json:
            self.commoditties, self.shares, self.crypto, _, _ = self.initialize(portfolio_json_to_compare, self.liquidity_json)
            self.portfolio_json = portfolio_json_to_compare

        if liquidity_json_to_compare != self.liquidity_json:
            _, _, _, self.liquidity, self.total_value = self.initialize(self.portfolio_json, liquidity_json_to_compare)
            self.liquidity_json = liquidity_json_to_compare

    def display(self):
        # Define a line separator for better readability
        separator = '-' * 50
        
        # Display Commodities
        print(f"\n{separator}")
        print(f"Commodities (Total: {self.commoditties['Total']} {self.quote_currency}):")
        for commodity, value in self.commoditties.items():
            if commodity != "Total":
                print(f"  {commodity}: {value} {self.quote_currency}")
        
        # Display Shares
        print(f"\n{separator}")
        print(f"Shares (Total: {self.shares['Total']} {self.quote_currency}):")
        for share, value in self.shares.items():
            if share != "Total":
                print(f"  {share}: {value} {self.quote_currency}")
        
        # Display Crypto
        print(f"\n{separator}")
        print(f"Crypto (Total: {self.crypto['Total']} {self.quote_currency}):")
        for crypto_asset, value in self.crypto.items():
            if crypto_asset != "Total":
                print(f"  {crypto_asset}: {value} {self.quote_currency}")
        
        # Display Liquidity
        print(f"\n{separator}")
        print(f"Liquidity (Total: {self.liquidity['Total']} {self.quote_currency}):")
        for currency, value in self.liquidity.items():
            if currency != "Total":
                print(f"  {currency}: {value} {self.quote_currency}")
        
        # Display Total Portfolio Value
        total_portfolio_value = (
            self.commoditties["Total"]
            + self.shares["Total"]
            + self.crypto["Total"]
            + self.liquidity["Total"]
        )
        
        print(f"\n{separator}")
        print(f"Total Portfolio Value: {total_portfolio_value} {self.quote_currency}")
        print(separator)



    def get_sunburst_data(self):
        labels = []
        parents = []
        values = []
        
        # Commodities
        for ticker, value in self.commoditties.items():
            if ticker == "Total":
                labels.append("Commodities")
                parents.append("")
                values.append(value)
            else:
                labels.append(ticker)
                parents.append("Commodities")
                values.append(value)
        
        # Shares
        for ticker, value in self.shares.items():
            if ticker == "Total":
                labels.append("Shares")
                parents.append("")
                values.append(value)
            else:
                labels.append(ticker)
                parents.append("Shares")
                values.append(value)
        
        # Crypto
        for ticker, value in self.crypto.items():
            if ticker == "Total":
                labels.append("Crypto")
                parents.append("")
                values.append(value)
            else:
                labels.append(ticker)
                parents.append("Crypto")
                values.append(value)
        
        # Liquidity
        for currency, value in self.liquidity.items():
            if currency == "Total":
                labels.append("Liquidity")
                parents.append("")
                values.append(value)
            else:
                labels.append(currency)
                parents.append("Liquidity")
                values.append(value)

        return labels, parents, values

    def create_interactive_sunburst(self):
        labels, parents, values = self.get_sunburst_data()
        
        fig = go.Figure(go.Sunburst(
            labels=labels,
            parents=parents,
            values=values,
            branchvalues="total",
            hovertemplate='<b>%{label}</b><br>Value: %{value:.2f} ' + self.quote_currency + '<br>Percentage: %{percentRoot:.2%}<extra></extra>'
        ))
        
        fig.update_layout(
            title="Interactive Portfolio Sunburst Chart",
            hoverlabel=dict(
                bgcolor="white",
                font_size=12,
                font_family="Rockwell"
            )
        )
        
        fig.show()