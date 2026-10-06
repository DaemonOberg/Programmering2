# Weather API

Ett väder-API byggt med Flask som hämtar aktuellt väder för en stad.

API:t använder Open-Meteo för att hitta stadens koordinater och sedan hämta aktuellt väder.

## Starta API:t

Starta Flask-servern med:

```powershell
flask --app "lektion1/weather_api/app.py" run
```

Servern körs på:

```text
http://127.0.0.1:5000
```

## Användning

Skriv en stad efter `/api/weather/`:

```text
http://127.0.0.1:5000/api/weather/Stockholm
```

Du kan byta ut `Stockholm` mot en annan stad.

## Exempel på svar

API:t returnerar stad, temperatur och väderförhållande som JSON:

```json
{
    "city": "Stockholm",
    "temperature": "16.2°C",
    "condition": "Overcast"
}
```

## Hur API:t fungerar

Först skickas stadens namn till Open-Meteos Geocoding API för att hämta:

- Latitude
- Longitude

Koordinaterna skickas sedan till Open-Meteos Weather API för att hämta:

- Aktuell temperatur
- Väderkod

Väderkoden översätts med `match` och `case` till text som till exempel:

- Clear sky
- Partly cloudy
- Overcast
- Rain
- Snow
- Thunderstorm