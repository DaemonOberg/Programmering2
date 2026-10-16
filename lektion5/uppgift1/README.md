# Lektion 5 – API-klient med Python

## Uppgift 1 – Enskild uppgift

### Beskrivning

I den här uppgiften har jag skapat en API-klient med Python som hämtar elpriser från ett öppet API.

Programmet hanterar olika fel som kan uppstå vid API-anrop och sparar informationen i en CSV-fil med hjälp av Pandas.

## Bibliotek

Jag använder två bibliotek:

- **requests** – För att hämta information från API:et.
- **pandas** – För att skapa tabeller och spara information som CSV.

```python
import pandas as pd
import requests
```

## 1. Hämta information från API:et

Jag använder API:et från [Elpriset Just Nu](https://www.elprisetjustnu.se/).

```python
url = "https://www.elprisetjustnu.se/api/v1/prices/2026/03-15_SE3.json"
```

Adressen hämtar elpriser för den 15 mars 2026 i elområde SE3.

```python
response = requests.get(url, timeout=5)
```

- `requests.get()` skickar en förfrågan till servern.
- `timeout=5` gör att programmet inte väntar obegränsat på servern.
- `response` sparar serverns svar.

## 2. Kontrollera HTTP-status

```python
response.raise_for_status()
```

Den här raden kontrollerar om servern har svarat med ett HTTP-fel.

Exempel på statuskoder:

- **200** – Förfrågan lyckades.
- **404** – Informationen hittades inte.
- **500** – Serverfel.

Om ett HTTP-fel upptäcks kan det fångas med `except requests.HTTPError`.

## 3. Läsa JSON-data

```python
data = response.json()
```

API:et skickar tillbaka information i JSON-format.

Med `.json()` omvandlas informationen till Python-data som programmet kan arbeta med.

## 4. Skapa en DataFrame

```python
df = pd.DataFrame(data)
```

Med Pandas omvandlar jag informationen till en tabell.

Tabellen innehåller:

- Elpris i SEK per kWh.
- Elpris i EUR per kWh.
- Växelkurs.
- Starttid.
- Sluttid.

När jag testade programmet fick jag **96 rader och 5 kolumner**.

Det beror på att API:et visar ett elpris var 15:e minut.

## 5. Spara informationen som CSV

```python
df.to_csv("lektion5/uppgift1/priser.csv", index=False)
```

Den här raden sparar tabellen i en CSV-fil.

- `lektion5/uppgift1/priser.csv` anger var filen ska sparas när programmet körs från projektets huvudmapp.
- `index=False` gör att Pandas inte sparar radnumren som en extra kolumn.

Jag använder också:

```python
print(df)
```

för att visa tabellen i terminalen.

## 6. Felhantering med try och except

Jag använder `try` och `except` för att hantera fel utan att programmet kraschar okontrollerat.

### HTTP-fel

```python
except requests.HTTPError:
    print("Ett HTTP-fel uppstod")
```

Hanterar HTTP-fel, exempelvis 404.

### Anslutningsfel

```python
except requests.ConnectionError:
    print("Ingen kontakt med servern")
```

Hanterar problem med anslutningen till servern.

### Timeout

```python
except requests.Timeout:
    print("Svaret dröjde för länge")
```

Hanterar situationer där ett API-anrop tar för lång tid.

### Ogiltig JSON

```python
except ValueError:
    print("200 ok men trasig JSON")
```

Hanterar bland annat situationer där serverns svar inte kan läsas som giltig JSON.

## 7. Tester

Jag har testat följande:

| Test | Resultat |
|---|---|
| Vanligt API-anrop | Lyckades, statuskod 200 |
| Ogiltigt datum i URL:en | HTTP-fel fångades |
| Anslutningsfel | Felmeddelande visades |
| Mycket kort timeout | Timeout-fel fångades |
| Ogiltig JSON | ValueError fångades |
| CSV-export | Elpriser sparades i priser.csv |

### Test av timeout

För att testa timeout ändrade jag tillfälligt:

```python
timeout=5
```

till:

```python
timeout=0.003
```

Det gjorde att programmet fick för kort tid att vänta på servern.

Terminalen visade:

```text
Svaret dröjde för länge
```

Efter testet återställde jag `timeout=5`.

### Test av HTTP-fel

Jag ändrade tillfälligt datumet i URL:en till ett ogiltigt datum:

```text
2026/99-99_SE3.json
```

Terminalen visade:

```text
Ett HTTP-fel uppstod
```

Det visade att min HTTP-felhantering fungerade.

### Test av ogiltig JSON

Jag testade att läsa en text som inte var giltig JSON.

Terminalen visade:

```text
200 ok men trasig JSON
```

Det visade att `except ValueError` fungerade.

## 8. Projektstruktur

```text
lektion5/
└── uppgift1/
    ├── klient.py
    ├── priser.csv
    └── README.md
```

## 9. Köra programmet

Från huvudmappen `Programmering2` kör jag:

```powershell
python lektion5/uppgift1/klient.py
```

Programmet:

1. Kontaktar API:et.
2. Kontrollerar HTTP-statusen.
3. Läser JSON-informationen.
4. Skapar en DataFrame med Pandas.
5. Sparar informationen i `priser.csv`.
6. Skriver ut tabellen i terminalen.

Om något går fel visas ett felmeddelande.

## Sammanfattning

Under lektion 5 har jag lärt mig att:

- Hämta information från ett öppet API med requests.
- Använda timeout vid API-anrop.
- Kontrollera HTTP-statuskoder.
- Hantera olika fel med try och except.
- Läsa JSON-data.
- Skapa en DataFrame med Pandas.
- Spara information i en CSV-fil.
- Testa hur programmet reagerar när något går fel.

**Resultat:** Jag har byggt en API-klient som hämtar elpriser, hanterar vanliga fel och sparar informationen i en CSV-fil.