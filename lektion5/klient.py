import requests

url = "https://www.elprisetjustnu.se/api/v1/prices/2026/03-15_SE3.json"
try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    data = response.json()

except requests.HTTPError:
    print("Ett HTTP-fel uppstod")
except requests.ConnectionError:
    print("Ingen kontakt med servern")
except requests.Timeout:
    print("Svaret dröjde för länge")
except ValueError:
    print("200 ok men trasig JSON")
