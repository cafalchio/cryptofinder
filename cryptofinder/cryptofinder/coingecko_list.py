import requests

url = "https://api.coingecko.com/api/v3/coins/list"
headers = {"x-cg-pro-api-key": "API-KEY"}
response = requests.get(url, headers=headers)
print(len((response.text).split(",")))