import sqlite3
import os

import numpy as np
import requests


api_key="20155216ZtEFPdQFOwcBowmWKInkJyTKzRiLL"

def main():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    strat_db_path = os.path.join(BASE_DIR, "strategy.db")
    conn_strat = sqlite3.connect(strat_db_path, check_same_thread=False)
    curs_strat = conn_strat.cursor()

    stock=[row[0] for row in curs_strat.execute(f"SELECT stock_name FROM portfolio").fetchall()]
    quantity=[row[0] for row in curs_strat.execute(f"SELECT quantity FROM portfolio").fetchall()]
    sum_=0
    for x in quantity:
        sum_+=x

    percentages=[round((x/sum_),5) for x in quantity]
    shares = dict( zip(stock, percentages))
    print(shares)

    url = "https://demo.trading212.com/api/v0/equity/pies"

    payload = {
      "dividendCashAction": "REINVEST",
      "endDate": "2019-08-24T14:15:22Z",
      "goal": 0,
      "icon": "Home",

      "instrumentShares":shares,
      "name": "portfolio"
    }

    headers = {
      "Content-Type": "application/json",
      "Authorization": api_key
    }

    response = requests.post(url, json=payload, headers=headers)

    data = response.json()
    print(data)


if __name__ == '__main__':
    main()