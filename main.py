import pandas as pd
import openbb
import riskfolio as rp

# Get new highs
new_highs = openbb.stocks.screener.screener_data("new_high")

new_highs = pd.read_csv("QS002-automate-trades/new_highs.csv")

port_data = new_highs[(new_highs.Price>15) & (new_highs.Country == "USA")]

port_data

tickers = port_data.Ticker.tolist()
tickers

# Get prices and returns

data = openbb.economy.index(tickers, start_date = "2016-01-01", end_date="2019-12-30")

data

returns = data.pct_change()[1:]

returns.dropna(how="any", axis=1, inplace=True)

returns

# Risk Portfolio

port = rp.Portfolio(returns=returns)

port.assets_stats(method_mu='hist', method_cov='hist', d=0.94)

port.lowerret = 0.0008

w_rp_c = port.rp_optimization(
    model = "Classic",
    rm = "MV",
    hist = True,
    rf = 0,
    b = None
)

w_rp_c

port_val = 10_000

w_rp_c["invest_amt"] = w_rp_c * port_val

w_rp_c["last_price"] = data.iloc[-1]

w_rp_c["shares"] = (w_rp_c.invest_amt / w_rp_c.last_price).astype(int)

w_rp_c
