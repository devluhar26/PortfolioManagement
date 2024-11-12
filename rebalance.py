import requests
headers = {
  "Content-Type": "application/json",
  "Authorization": "20155216ZpCEwlxRBQEXFJzupJKWZkYRIQWnu"
}


output=[['APH', 21.45],['DBOEY', 11.27],['SSREY', 9.81],['ACGL', 9.32],['CICOF', 8.55]]
url = "https://demo.trading212.com/api/v0/equity/pies"
response = requests.get(url, headers=headers)
response.raise_for_status()
data = response.json()
array= [x["id"] for x in data]
id = array[0]
url = f"https://demo.trading212.com/api/v0/equity/pies/{id}"

payload = {"dividendCashAction": "REINVEST",
  "instrumentShares":output}



response = requests.post(url, json=payload, headers=headers)

data = response.json()
print(data)