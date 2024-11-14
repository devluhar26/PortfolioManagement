import requests
import yfinance as yf
all_stock = ['APH', 'DBOEY', 'SSREY', 'ACGL', 'CICOF', 'KSPI', 'MKL', 'EVVTY',
           'MOH', 'UTHR', 'SMCI', 'GMAB', 'SN', 'NBIX']

url = "https://demo.trading212.com/api/v0/equity/metadata/instruments"
headers = {"Authorization": "20155216ZpCEwlxRBQEXFJzupJKWZkYRIQWnu"}
response = requests.get(url, headers=headers)
data = response.json()
selected_isin = []

for desired_stock in all_stock:
    ticker = yf.Ticker(desired_stock)
    isin = ticker.isin
    print(desired_stock)
    print(isin)
    if isin!="-":
        found=False
        temp=[]
        for x in data:
            if (x["shortName"]==desired_stock) :
                if x["isin"]==isin:
                    print(x)
                    selected_isin.append(x["ticker"])
                    found=True
                else:
                    temp.append(x)
                    print(x)
        if found==False:
            if len(temp)==0:
                print("no stock found")
            elif len(temp)==1:
                selected_isin.append(temp[0]["ticker"])
            else:
                selected=int(input("which stock would you like to select?: "))
                selected_isin.append(temp[selected]["ticker"])
    else:
        temp=[]
        for x in data:
            if (x["shortName"] == desired_stock):
                temp.append(x)
                print(x)
        if temp!=[]:
            if len(temp)==1:
                print(temp[0])
                selected_isin.append(temp[0]["ticker"])

            else:
                selected=input("which stock would you like to select?: ")
                print(temp[int(selected)])
                selected_isin.append(temp[int(selected)]["ticker"])
        else:
            print(desired_stock," not found in the system")
            selected_isin.append("")
            pass

print(selected_isin)