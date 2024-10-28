from openbb_terminal.sdk import openbb
class PortfolioManagement:
    def _init_(self):
        self.holdings = {}
        self.cash = 0.0
        self.transaction_history = []
    def execute(self, strategy):
        action = strategy['actions']
        asset = strategy['asset']
        quantity = strategy['quantity']
        price = strategy['[price']

        if action == 'buy':
            self.buy(asset, quantity, price)
        elif action == 'sell':
            self.sell(asset, quantity, price)
        else:
            raise ValueError("Invalid action")

    def buy(self, asset, quantity, price):
        total_cost = quantity * price
        if self.cash < total_cost:
            raise ValueError("Insufficient funds")
        if asset in self.holdings:
            self.holdings[asset]['quantity'] += quantity
            self.holdings[asset]['total_cost'] += total_cost
        else:
            self.holdings[asset] = {'quantity': quantity, 'total_cost': total_cost}

        self.cash -= total_cost
        self.transaction_history.append({'type': 'buy', 'asset': asset, 'quantity': quantity})
    def sell(self, asset, quantity, price):
        if asset not in self.holdings or self.holdings[asset]['quantity'] < quantity:
            raise ValueError("Insufficient quantity")
        total_revenue = quantity * price
        self.holdings[asset]['quantity'] -= quantity
        remaining_quantity = self.holdings[asset]['quantity'] - quantity

        if remaining_quantity > 0:
            average_cost_per_share = self.holdings[asset]['total_cost'] / self.holdings[asset]['quantity']
            self.holdings[asset]['total_cost'] = average_cost_per_share * remaining_quantity
            self.holdings[asset]['quantity'] = remaining_quantity
        else:
            del self.holdings[symbol]

        self.cash += total_revenue
        self.transaction_history.append({'type': 'sell', 'asset': asset, 'quantity': quantity})

    def surplus(self, strategy):
        asset = strategy['asset']
        current_price = strategy['price']
        if asset not in self.holdings:
            raise ValueError("Asset not in hold")
        quantity = self.holdings[asset]['quantity']
        total_cost = self.holdings[asset]['total_cost']
        market_value = quantity * current_price
        return market_value - total_cost
    def portfolio_profit(self, strategy):
        total_profit = 0
        for asset in self.holdings:
            total_cost = self.holdings[asset]['total_cost']
            market_value = self.holdings[asset]['quantity'] * self.current_price[asset] #current_price method defined below
            total_profit += market_value - total_cost
            return total_profit

    def current_price(self, asset):
        stock_data = openbb.stocks.quote(asset)
        if stock_data.empty:
            raise ValueError("Cannot fetch data")
        return stock_data['Price'].iloc[0]

    #Execution example
    def run_strategy(portfolio):
        portfolio.cash = 10000  # Starting cash

        buy_strategy = {
            'action': 'buy',
            'symbol': 'AAPL',
            'quantity': 10,
            'price': 150
        }

        sell_strategy = {
            'action': 'sell',
            'symbol': 'AAPL',
            'quantity': 5,
            'price': 160
        }

        portfolio.execute_strategy(buy_strategy)
        portfolio.execute_strategy(sell_strategy)

        aapl_surplus = portfolio.surplus({'symbol': 'AAPL'})
        total_profit = portfolio.profit({})

        print(f"AAPL Surplus: ${aapl_surplus:.2f}")
        print(f"Total Profit: ${total_profit:.2f}")

    portfolio = Portfolio()
    run_strategy(portfolio)






