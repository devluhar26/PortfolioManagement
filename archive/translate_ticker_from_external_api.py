
import requests
query="AIR"
url = "https://financialmodelingprep.com/api/v3/search?query="+query+"&apikey=wWpqroVfSsiNgZqOD0adxPMu0P6YRKC2"
response = requests.get(url)

data = response.json()
print(data)
