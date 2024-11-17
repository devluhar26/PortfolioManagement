import requests
import yfinance as yf


class TickerTranslator:
    def __init__(self, api_key, stocks):
        self.api_key = api_key
        self.stocks = stocks
        self.headers = {"Authorization": self.api_key}
        self.url = "https://demo.trading212.com/api/v0/equity/metadata/instruments"
        self.data = self._fetch_data()
        self.selected_isin = []

    def _fetch_data(self):
        response = requests.get(self.url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def _fetch_isin(self, stock):
        ticker = yf.Ticker(stock)
        return ticker.isin

    def _process_stock(self, stock, isin):
        print(f"Processing stock: {stock}")
        print(f"ISIN: {isin if isin else 'Unavailable'}")

        if isin != "-":
            return self._match_with_isin(stock, isin)
        else:
            return self._search_by_short_name(stock)

    def _match_with_isin(self, stock, isin):
        matches = []
        for item in self.data:
            if item["shortName"] == stock:
                if item["isin"] == isin:
                    print(f"Exact match found: {item}")
                    return item["ticker"]
                matches.append(item)

        if matches:
            return self._resolve_multiple_matches(stock, matches)
        else:
            print(f"No match found for {stock}")
            return ""

    def _search_by_short_name(self, stock):
        matches = [item for item in self.data if item["shortName"] == stock]

        if len(matches) == 1:
            print(f"Single match found: {matches[0]}")
            return matches[0]["ticker"]
        elif len(matches) > 1:
            return self._resolve_multiple_matches(stock, matches)
        else:
            print(f"No match found for {stock}")
            return ""

    def _resolve_multiple_matches(self, stock, matches):
        print(f"Multiple matches found for {stock}:")
        for index, match in enumerate(matches):
            print(f"{index}: {match}")

        while True:
            try:
                selected_index = int(input(f"Which stock would you like to select for {stock} (Enter index)? "))
                if 0 <= selected_index < len(matches):
                    return matches[selected_index]["ticker"]
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def translate_tickers(self):

        for stock in self.stocks:
            isin = self._fetch_isin(stock)
            ticker = self._process_stock(stock, isin)
            self.selected_isin.append(ticker)
        return self.selected_isin

    def print_results(self):

        print("\nSelected ISINs:")
        print(self.selected_isin)


if __name__ == "__main__":
    # Inputs
    api_key = "20155216ZpCEwlxRBQEXFJzupJKWZkYRIQWnu"
    stocks = ['APH', 'DBOEY', 'SSREY', 'ACGL', 'CICOF', 'KSPI', 'MKL', 'EVVTY',
              'MOH', 'UTHR', 'SMCI', 'GMAB', 'SN', 'NBIX']

    # Initialize the translator
    translator = TickerTranslator(api_key, stocks)

    # Translate tickers and print results
    selected_tickers = translator.translate_tickers()
    translator.print_results()