import requests
from streamlit.web.cli import main_hello

def main(shares):
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
      "Authorization": "20155216ZpCEwlxRBQEXFJzupJKWZkYRIQWnu"
    }

    response = requests.post(url, json=payload, headers=headers)

    data = response.json()
    print(data)

    if data=={'code': 'InternalError'}:
        file = open("memory/pieinfo.txt", "r")

        id = file.read()
        url = "https://demo.trading212.com/api/v0/equity/pies/" + id

        headers = {"Authorization": "20155216ZpCEwlxRBQEXFJzupJKWZkYRIQWnu"}

        response = requests.get(url, headers=headers)

        data = response.json()
        print(data)
    else:
        file = open("memory/pieinfo.txt", "w")
        file.write(str(data["settings"]["id"]))
        file.close()
