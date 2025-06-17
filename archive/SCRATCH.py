import requests



api_key="20155216ZtEFPdQFOwcBowmWKInkJyTKzRiLL"
headers = {"Authorization": api_key}
url = "https://demo.trading212.com/api/v0/equity/metadata/instruments"

def fetch_data():
  response = requests.get(url, headers=headers)
  return response.json()
data=fetch_data()
print(data)