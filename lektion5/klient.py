# Importerar Pandas för att hantera tabeller och spara CSV-filer
import pandas as pd

# Importerar Requests för att hämta information från ett API
import requests

# Adressen till API:et som hämtar elpriser för 15 mars 2026 i elområde SE3
url = "https://www.elprisetjustnu.se/api/v1/prices/2026/03-15_SE3.json"

# Försöker hämta och behandla informationen från API:et
try:
    # Skickar en GET-förfrågan med en timeout på 5 sekunder
    response = requests.get(url, timeout=5)

    # Kontrollerar om servern svarade med ett HTTP-fel, exempelvis 404
    response.raise_for_status()

    # Omvandlar JSON-svaret till Python-data
    data = response.json()

    # Skapar en tabell (DataFrame) av informationen
    df = pd.DataFrame(data)

    # Sparar tabellen som en CSV-fil utan Pandas radnummer
    df.to_csv("lektion5/priser.csv", index=False)

    # Skriver ut tabellen i terminalen
    print(df)

# Fångar HTTP-fel, exempelvis 404 eller 500
except requests.HTTPError:
    print("Ett HTTP-fel uppstod")

# Fångar fel om programmet inte kan ansluta till servern
except requests.ConnectionError:
    print("Ingen kontakt med servern")

# Fångar fel om API-anropet tar för lång tid
except requests.Timeout:
    print("Svaret dröjde för länge")

# Fångar fel om JSON-svaret inte går att läsa
except ValueError:
    print("200 ok men trasig JSON")
