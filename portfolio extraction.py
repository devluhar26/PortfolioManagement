import requests
import yfinance as yf

class TradingDataHandler:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {"Authorization": self.api_key}

    def retrieve_all_pie_ids(self):
        url = "https://demo.trading212.com/api/v0/equity/pies"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        data = response.json()
        return [x["id"] for x in data]

    def get_pie_data(self):
        pie_ids = self.retrieve_all_pie_ids()
        pie_quantity = []
        pie_percentage = []
        stock_names = []

        for pie_id in pie_ids:
            print(f"Processing PIE ID: {pie_id}")
            url = f"https://demo.trading212.com/api/v0/equity/pies/{pie_id}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            total_value = sum(x["result"]["priceAvgValue"] for x in data["instruments"])

            for instrument in data["instruments"]:
                ticker = instrument["ticker"]
                stock_name = ticker[:-3]
                print(f"{ticker} is valid on Trading 212 with {instrument['ownedQuantity']} owned quantity and a percentage of {instrument['currentShare'] * 100:.2f}%.")
                print(f"Additional data: {instrument}")
                stock_names.append(stock_name)
                pie_quantity.append([ticker, instrument["ownedQuantity"]])
                pie_percentage.append([ticker, instrument["result"]["priceAvgValue"] / total_value])

        return pie_quantity, pie_percentage, stock_names

    def download_stock_data(self, stock_names):
        for stock in stock_names:
            try:
                data = yf.download(stock[:-1] + "." + stock[-1:], start='2018-01-01', end=None)
                if data.empty:
                    raise ValueError("Empty DataFrame")
                print(f"Downloaded data for {stock}")
                print(data.head())
            except Exception as e:
                print(f"Failed to download {stock}: {e}")

if __name__ == "__main__":
    api_key = "20155216ZpCEwlxRBQEXFJzupJKWZkYRIQWnu"
    trading_data_handler = TradingDataHandler(api_key)

    pie_quantity, pie_percentage, stock_names = trading_data_handler.get_pie_data()

    for stock in stock_names:
        trading_212_ticker = stock + ".EQ"
        print(f"{trading_212_ticker} is valid on Trading 212.")

    trading_data_handler.download_stock_data(stock_names)