import requests

url = "https://demo.trading212.com/api/v0/equity/metadata/instruments"

headers = {"Authorization": "20155216ZpCEwlxRBQEXFJzupJKWZkYRIQWnu"}

response = requests.get(url, headers=headers)

data = response.json()
print(data)