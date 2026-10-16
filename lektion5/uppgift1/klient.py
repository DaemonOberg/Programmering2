import pandas as pd
import requests

url = "https://www.elprisetjustnu.se/api/v1/prices/2026/03-15_SE3.json"
try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data)
    df.to_csv("lektion5/uppgift1/priser.csv", index=False)
    print(df)
except requests.HTTPError:
    print("Ett HTTP-fel uppstod")
except requests.ConnectionError:
    print("Ingen kontakt med servern")
except requests.Timeout:
    print("Svaret dröjde för länge")
except ValueError:
    print("200 ok men trasig JSON")
