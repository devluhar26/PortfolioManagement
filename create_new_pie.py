import requests
def main(shares):
    url = "https://demo.trading212.com/api/v0/equity/pies"

    payload = {
      "dividendCashAction": "REINVEST",
      "endDate": "2019-08-24T14:15:22Z",
      "goal": 0,
      "icon": "Home",

      "instrumentShares":shares,
      "name": "string1"
    }

    headers = {
      "Content-Type": "application/json",
      "Authorization": "20155216ZpCEwlxRBQEXFJzupJKWZkYRIQWnu"
    }

    response = requests.post(url, json=payload, headers=headers)

    data = response.json()
    print(data)