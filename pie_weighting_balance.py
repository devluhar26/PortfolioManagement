import ast
import sqlite3
import os
import create_new_pie
import numpy as np

import translate_tickers_from_instrument_list
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
strat_db_path = os.path.join(BASE_DIR, "strategies.db")
conn_strat = sqlite3.connect(strat_db_path, check_same_thread=False)
curs_strat = conn_strat.cursor()

weighting=[row[0] for row in curs_strat.execute(f"SELECT weighting FROM strat").fetchall()]
strat_name=[row[0] for row in curs_strat.execute(f"SELECT strategy_name FROM strat").fetchall()]
stocks = []
percentages = []
sum_=0
for x in range(len(weighting)):

    weight=weighting[x]/100
    file = open("memory/" + strat_name[x] + ".txt", "r")
    array=ast.literal_eval(file.read().strip())
    for x in array:
        stocks.append(x[0])
        percentages.append(round((x[1]*weight)/100,5))

    file.close()
new_stock=translate_tickers_from_instrument_list.main(stocks)
dictionary = dict( zip(new_stock, percentages))
print(dictionary)
create_new_pie.main(dictionary)