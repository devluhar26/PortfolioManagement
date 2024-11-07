import requests
import yfinance as yf
all_stock = ['APH', 'DBOEY', 'SSREY', 'ACGL', 'CICOF', 'KSPI', 'MKL', 'EVVTY',
           'MOH', 'UTHR', 'SMCI', 'GMAB', 'SN', 'NBIX']
url = "https://demo.trading212.com/api/v0/equity/metadata/instruments"
headers = {"Authorization": "20155216ZpCEwlxRBQEXFJzupJKWZkYRIQWnu"}
response = requests.get(url, headers=headers)
data = response.json()
for desired_stock in all_stock:
    ticker = yf.Ticker(desired_stock)
    isin = ticker.isin
    print(desired_stock)
    print(isin)
    selected_isin=[]
    if isin!="-":
        for x in data:
            if (x["shortName"]==desired_stock) :
                if x["isin"]==isin:
                    print(x)
    else:
        temp=[]
        for x in data:
            if (x["shortName"] == desired_stock):
                temp.append(x)
                print(x)
        if temp!=[]:
            if len(temp)==1:
                print(temp[0])
            else:
                selected=input("which stock would you like to select?")
                print(temp[int(selected)])
        else:
            print(desired_stock," not found in the system")
            pass

