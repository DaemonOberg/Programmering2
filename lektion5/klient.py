import requests

url = "https://www.elprisetjustnu.se/api/v1/prices/2026/03-15_SE3.json"

response = requests.get(url, timeout=5)
print(response.status_code)