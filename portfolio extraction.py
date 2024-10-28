import requests
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

headers = {"Authorization": "20155216ZpCEwlxRBQEXFJzupJKWZkYRIQWnu"}

def retrieve_all_pie_id():
    url = "https://demo.trading212.com/api/v0/equity/pies"
    response = requests.get(url, headers=headers)
    data = response.json()
    ids=[]
    for x in data:
        ids.append(x["id"])
    return ids

def get_pie_data():
    ids=retrieve_all_pie_id()
    for id in ids:
        print(id)
        url = "https://demo.trading212.com/api/v0/equity/pies/" + str(id)
        response = requests.get(url, headers=headers)

        data = response.json()
        sum=0
        for x in data["instruments"]:
            sum+=x["result"]["priceAvgValue"]
        pie_percentage=[]
        pie_quantity=[]
        stock_name=[]
        for x in data["instruments"]:
            print(x)
            print(x["ticker"],": ",x["result"]["priceAvgValue"]*100/sum)
            stock_name.append(x["ticker"][:-3])
            pie_quantity.append([x["ticker"],x["ownedQuantity"]])
            pie_percentage.append([x["ticker"],x["result"]["priceAvgValue"]/sum])
        return pie_quantity, pie_percentage,stock_name

pie_quantity, pie_percentage, stock_name=get_pie_data()
for x in stock_name:
    data = yf.download(x[:-1]+"."+x[-1:], start='2018-01-01', end=None)
    print(data)