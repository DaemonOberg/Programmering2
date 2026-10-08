
# Weather App - Flask och Open-Meteo

I den här uppgiften skapade jag en väderapp med hjälp av Flask, HTML och CSS.

Jag använde Open-Meteo API för att hämta väderinformation om olika städer, bland annat temperatur och väderförhållanden.

Jag använde även Jinja2 för att visa väderinformationen på HTML-sidan och Requests för att skicka förfrågningar till API:erna.

## Mappstruktur

```text
weather_project/
│
├── templates/
│   └── index.html
│
└── app.py
```

## Flask

Jag importerade Flask och de funktioner som behövs:

```python
from flask import Flask, jsonify, render_template, request
```

Sedan skapade jag Flask-applikationen:

```python
app = Flask(__name__)
```

Startsidan skapas med:

```python
@app.route("/")
def index():
```

Jag använde `request.args.get()` för att hämta stadsnamnet från användarens sökning:

```python
city = request.args.get("city")
```

Sedan skapade jag variabeln `result` och gav den värdet `None`:

```python
result = None
```

Det betyder att det inte finns någon väderinformation innan användaren har sökt efter en stad.

Sedan kontrollerar programmet att användaren har skrivit ett stadsnamn som bara innehåller bokstäver:

```python
if city and city.isalpha():
    result = get_weather(city)
```

`isalpha()` kontrollerar om strängen bara innehåller bokstäver.

Om kontrollen godkänns anropas funktionen `get_weather(city)` som hämtar väderinformationen.

Sedan skickas stadsnamnet och resultatet till HTML-sidan:

```python
return render_template("index.html", city=city, result=result)
```

Det betyder att `index.html` får tillgång till variablerna `city` och `result`.

## HTML och GET

I `index.html` skapade jag ett sökfält där användaren kan skriva in en stad:

```html
<form method="GET">
    <input type="text" name="city" placeholder="Enter a city..." required>
</form>
```

`method="GET"` gör att informationen skickas genom URL:en.

`name="city"` bestämmer namnet på parametern som skickas till Flask.

`required` gör att användaren måste skriva något innan formuläret kan skickas.

När användaren exempelvis söker efter Stockholm blir adressen:

```text
http://127.0.0.1:5000/?city=Stockholm
```

Flask hämtar sedan stadsnamnet med:

```python
city = request.args.get("city")
```

## Requests och API

Jag importerade Requests:

```python
import requests
```

Requests används för att skicka HTTP-förfrågningar till externa API:er.

Jag skapade en funktion som hämtar väderinformation:

```python
def get_weather(city):
```

Funktionen tar emot ett stadsnamn och använder Open-Meteo för att hämta information om staden.

## Open-Meteo Geocoding API

Först använder jag Open-Meteos Geocoding API för att hitta stadens koordinater.

```python
geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
```

Sedan skickar jag med stadsnamnet som en parameter:

```python
params = {"name": city}
```

Jag skickar en GET-förfrågan:

```python
response = requests.get(geocoding_url, params=params)
```

Sedan gör jag om JSON-svaret till Python-data:

```python
data = response.json()
```

`response.json()` gör att jag kan använda informationen som exempelvis dictionaries och listor i Python.

## Dictionaries och listor

För att hämta det första resultatet från API:et använder jag:

```python
first_result = data["results"][0]
```

`["results"]` hämtar listan med städer från dictionaryn.

`[0]` hämtar det första elementet i listan.

Sedan hämtar jag stadens koordinater:

```python
latitude = first_result["latitude"]
longitude = first_result["longitude"]
```

`latitude` är stadens breddgrad och `longitude` är stadens längdgrad.

Dessa används sedan för att hämta väderinformationen.

## Kontroll av stadsnamn

Jag märkte att Open-Meteo ibland kunde hitta en annan stad än den användaren sökte efter.

Exempelvis kunde en sökning på `ääö` ge ett resultat för staden Anaco.

För att förhindra detta lade jag till en kontroll:

```python
if "results" in data:
    first_result = data["results"][0]

    if first_result["name"].casefold() != city.casefold():
        return None

    latitude = first_result["latitude"]
    longitude = first_result["longitude"]

else:
    return None
```

`if "results" in data` kontrollerar att API:et har hittat ett resultat.

`.casefold()` används för att jämföra stadsnamnen utan att skilja mellan stora och små bokstäver.

`!=` betyder att värdena inte är lika.

Om stadsnamnen inte matchar används:

```python
return None
```

Det gör att funktionen avslutas utan att skicka tillbaka någon väderinformation.

Om API:et inte hittar någon stad används också `return None`.

Den här kontrollen kräver att stadsnamnen matchar, vilket innebär att vissa alternativa stavningar inte fungerar.

## Open-Meteo Weather API

När stadens koordinater har hämtats använder jag Open-Meteos väder-API.

```python
weather_url = "https://api.open-meteo.com/v1/forecast"
```

Sedan skickar jag med koordinaterna och ber om aktuellt väder:

```python
params = {
    "latitude": latitude,
    "longitude": longitude,
    "current_weather": True
}
```

Jag skickar en ny GET-förfrågan:

```python
weather_response = requests.get(weather_url, params=params)
```

Sedan gör jag om JSON-svaret till Python-data:

```python
weather_data = weather_response.json()
```

För att hämta temperaturen och väderkoden använder jag:

```python
temperature = weather_data["current_weather"]["temperature"]
condition = weather_data["current_weather"]["weathercode"]
```

`temperature` innehåller temperaturen och `condition` innehåller väderkoden.

## Match och Case

Open-Meteo skickar väderförhållanden som nummer.

Jag använde `match` och `case` för att översätta numren till text:

```python
match condition:
    case 0:
        condition = "Clear sky"
    case 1:
        condition = "Mainly clear"
    case 2:
        condition = "Partly cloudy"
    case 3:
        condition = "Overcast"
    case 45:
        condition = "Fog"
    case 61:
        condition = "Light rain"
    case 71:
        condition = "Light snow"
    case 95:
        condition = "Thunderstorm"
    case _:
        condition = "Unknown"
```

`match` jämför värdet i `condition` med olika `case`.

När ett värde matchar ändras väderkoden till en textbeskrivning.

`case _` används om väderkoden inte matchar något av de andra alternativen.

Jag lade även till fler väderkoder för exempelvis regn, snö, dimma och åska.

## Return och Dictionary

När väderinformationen har hämtats skickar funktionen tillbaka en dictionary:

```python
return {
    "city": city,
    "temperature": f"{temperature}°C",
    "condition": condition
}
```

Dictionaryn innehåller tre nycklar:

- `city` innehåller stadsnamnet.
- `temperature` innehåller temperaturen i Celsius.
- `condition` innehåller väderförhållandet.

Jag använde även en f-string:

```python
f"{temperature}°C"
```

Det gör att temperaturens värde kombineras med texten `°C`.

`return` skickar tillbaka dictionaryn till den funktion som anropade `get_weather()`.

## Jinja2

I `index.html` använder jag Jinja2 för att visa väderinformationen:

```html
<div class="weather-info">
    {% if result %}
        <p>{{ city }}</p>
    {% endif %}

    {% if result %}
        <p>{{ result.temperature }}</p>
        <p>{{ result.condition }}</p>
    {% endif %}

    {% if city and not result %}
        <p>City not found</p>
    {% endif %}
</div>
```

`{% if result %}` kontrollerar om det finns någon väderinformation att visa.

`{{ city }}` visar stadsnamnet.

`{{ result.temperature }}` visar temperaturen.

`{{ result.condition }}` visar väderförhållandet.

`{% endif %}` avslutar en `if`-sats i Jinja2.

Jag använde även:

```html
{% if city and not result %}
    <p>City not found</p>
{% endif %}
```

Det gör att ett felmeddelande visas om användaren har sökt efter en stad men inget giltigt resultat hittades.

## CSS

Jag använde CSS för att styla hemsidan.

För att centrera innehållet och ändra bakgrundsfärgen använde jag:

```css
body {
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 30px;
    min-height: 100vh;
    flex-direction: column;
    background-color: #152C49;
    color: white;
}
```

`display: flex` aktiverar Flexbox.

`justify-content: center` och `align-items: center` används för att centrera innehållet.

`flex-direction: column` gör att elementen placeras under varandra.

`background-color` ändrar bakgrundsfärgen och `color` ändrar textfärgen.

Jag ändrade även storleken på sökfältet:

```css
input {
    font-size: 20px;
    padding: 12px;
    width: 300px;
}
```

För att visa väderinformationen bredvid varandra använde jag:

```css
.weather-info {
    display: flex;
    flex-direction: row;
    gap: 20px;
    align-items: center;
    font-size: 25px;
}
```

`flex-direction: row` gör att elementen placeras bredvid varandra.

`gap: 20px` skapar mellanrum mellan elementen.

## JSON och egen API-route

Jag skapade även en egen API-route som returnerar väderinformationen som JSON:

```python
@app.route("/api/weather/<city>")
def weather(city):
    data = get_weather(city)
    return jsonify(data)
```

`<city>` gör att stadsnamnet kan anges direkt i URL:en.

`get_weather(city)` hämtar väderinformationen.

`jsonify(data)` gör om resultatet till ett JSON-svar.

Exempel på URL:

```text
http://127.0.0.1:5000/api/weather/Stockholm
```

Ett exempel på JSON-svaret:

```json
{
    "city": "Stockholm",
    "temperature": "13.9°C",
    "condition": "Overcast"
}
```

Temperaturen och väderförhållandet ändras beroende på det aktuella vädret.

## Starta programmet

Från mappen `Programmering2` kan programmet startas med:

```powershell
flask --app "weather_project/app.py" run
```

Öppna sedan adressen som Flask visar i terminalen:

```text
http://127.0.0.1:5000/
```

För att aktivera automatisk omladdning under utvecklingen kan jag använda:

```powershell
flask --app "weather_project/app.py" run --debug
```

## Resultat

Webbsidan visar:

- Ett sökfält där användaren kan skriva in en stad.
- Stadens namn när ett giltigt resultat hittas.
- Stadens aktuella temperatur i Celsius.
- Väderförhållandet i textform.
- Felmeddelandet "City not found" om sökningen inte ger ett giltigt resultat.
- En mörkblå bakgrund med vit text.
- Väderinformationen placerad bredvid varandra med hjälp av Flexbox.

Jag skapade även en API-route som gör det möjligt att hämta väderinformationen som JSON.
