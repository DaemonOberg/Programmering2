
# Elpris Tracker - Flask och Elpriset Just Nu

I den här uppgiften skapade jag en webbapplikation med hjälp av Flask, HTML, CSS och Bootstrap.

Jag använde Elpriset Just Nus API för att hämta elpriser baserat på ett datum och ett elområde som användaren väljer.

Jag använde även Pandas för att omvandla informationen från API:et till en tabell och Jinja2 för att visa tabellen på webbsidan.

## Mappstruktur

Jag delade upp projektet i olika filer för att hålla Python, HTML och CSS separerade.

```text
lektion4/
│
├── static/
│   └── style.css
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── navbar.html
│   ├── footer.html
│   ├── prices.html
│   └── error.html
│
├── app.py
└── README.md
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
    return render_template("index.html")
```

`@app.route("/")` bestämmer vilken adress som ska användas för startsidan.

`render_template()` används för att visa HTML-filer från mappen `templates`.

## HTML och POST

I `index.html` skapade jag ett formulär där användaren kan välja år, månad, dag och elområde.

Jag använde `select` för att användaren ska kunna välja mellan olika alternativ.

Formuläret skickar informationen till `/api` med POST:

```html
<form method="POST" action="/api">
```

`method="POST"` betyder att informationen skickas till servern i en POST-förfrågan.

`action="/api"` bestämmer vilken route som ska ta emot informationen.

För att välja dag använde jag en Jinja2-loop:

```html
<label for="day">Dag</label>
<select id="day" name="day" class="form-select" required>
    <option value="" disabled selected>Välj Dag</option>
    {% for day in range(1, 32) %}
        <option value="{{ day }}">{{ day }}</option>
    {% endfor %}
</select>
```

`range(1, 32)` skapar alternativen från 1 till 31.

`{{ day }}` används för att visa varje dag som ett alternativ.

`required` gör att användaren måste välja ett alternativ innan formuläret skickas.

## Flask API-route

Jag skapade en egen route som heter `/api`:

```python
@app.route("/api", methods=["GET", "POST"])
def api():
```

Den kan ta emot både GET och POST.

Jag använder en `if`-sats för att kontrollera om användaren har skickat formuläret:

```python
if request.method == "POST":
```

Sedan hämtar jag användarens val:

```python
year = request.form.get("year")
month = request.form.get("month")
day = request.form.get("day")
price_class = request.form.get("price_class")
```

`request.form.get()` hämtar informationen från formuläret.

Variablerna innehåller det år, den månad, den dag och det elområde som användaren har valt.

Om någon besöker `/api` med GET returnerar programmet istället ett JSON-meddelande:

```python
return jsonify({"message": "Mitt API fungerar!"})
```

`jsonify()` används för att skapa ett JSON-svar.

## Validering av indata

Jag lade till validering för att kontrollera att användaren skickar giltiga värden.

Först kontrollerar jag att elområdet är ett av de fyra tillåtna alternativen:

```python
if price_class not in ["SE1", "SE2", "SE3", "SE4"]:
    return render_template("error.html"), 400
```

`not in` kontrollerar om värdet saknas i listan.

Om elområdet inte är giltigt visas felsidan med HTTP-statuskoden `400`.

Jag använde även `date` för att kontrollera datumet:

```python
from datetime import date
```

Sedan kontrollerar jag att datumet existerar:

```python
try:
    date(int(year), int(month), int(day))
except (ValueError, TypeError):
    return render_template("error.html"), 400
```

`int()` omvandlar värdena från formuläret till heltal.

`date()` kontrollerar att datumet är giltigt och tar även hänsyn till skottår.

Om användaren exempelvis väljer 31 februari kommer kontrollen att ge ett `ValueError`.

`except` fångar felet och visar felsidan.

## Requests och externt API

Jag använde Requests för att hämta elpriser från Elpriset Just Nus API.

Först importerade jag biblioteket:

```python
import requests
```

Eftersom API:et kräver att dagen skrivs med två siffror använde jag:

```python
day = day.zfill(2)
```

`zfill(2)` lägger till en nolla framför dagen om den bara innehåller en siffra.

Exempelvis blir `1` till `01`.

Sedan skapade jag URL:en med en f-string:

```python
url = f"https://www.elprisetjustnu.se/api/v1/prices/{year}/{month}-{day}_{price_class}.json"
```

En f-string gör att jag kan lägga in variabler direkt i en sträng.

URL:en ändras beroende på vilket datum och elområde användaren har valt.

Jag skickar sedan en GET-förfrågan till API:et:

```python
response = requests.get(url, timeout=10)
```

`requests.get()` hämtar information från API:et.

`timeout=10` betyder att programmet väntar högst 10 sekunder på svaret innan en timeout kan uppstå.

API:et kräver ingen API-nyckel.

## Felhantering

Jag lade till en kontroll för att hantera situationer där API:et inte hittar några elpriser.

```python
if response.status_code == 404:
    return render_template("error.html"), 404
```

`response.status_code` innehåller HTTP-statuskoden från API:et.

Om API:et svarar med `404` visas min `error.html`.

Jag använder två olika statuskoder:

- `400` om användaren skickar ett ogiltigt datum eller elområde.
- `404` om API:et inte hittar några elpriser.

I `error.html` visar jag ett felmeddelande som passar båda situationerna.

## JSON och Pandas

När API:et har skickat tillbaka informationen använder jag:

```python
data = response.json()
```

`response.json()` omvandlar JSON-svaret till Python-data.

Sedan importerade jag Pandas:

```python
import pandas as pd
```

Jag använder Pandas för att skapa en DataFrame:

```python
df = pd.DataFrame(data)
```

En DataFrame organiserar informationen i rader och kolumner.

Sedan omvandlar jag den till en HTML-tabell:

```python
html_table = df.to_html(
    classes="table table-striped table-bordered text-start", index=False
)
```

`to_html()` omvandlar DataFrame till HTML.

`classes` används för att lägga till Bootstrap-klasser på tabellen.

`table-striped` gör att tabellens rader får växlande bakgrundsfärg.

`table-bordered` lägger till ramar runt tabellens celler.

`index=False` gör att Pandas inte visar sitt eget index i tabellen.

Sedan skickar jag tabellen till HTML-sidan:

```python
return render_template("prices.html", table=html_table)
```

## Jinja2

Jag använde Jinja2 för att koppla samman mina HTML-filer.

I `base.html` skapade jag en gemensam grundstruktur:

```html
{% block content %}{% endblock %}
```

`block content` bestämmer var innehållet från de andra HTML-filerna ska placeras.

De andra sidorna använder:

```html
{% extends "base.html" %}
```

Det gör att de ärver strukturen från `base.html`.

Jag använde även `include` för att dela upp navigationsmenyn och footern i egna filer:

```html
{% include "navbar.html" %}
{% include "footer.html" %}
```

I `prices.html` visar jag tabellen med:

```html
{{ table | safe }}
```

`{{ table }}` innehåller HTML-tabellen som skickas från Flask.

`safe` gör att Jinja2 tolkar innehållet som HTML istället för att visa HTML-taggarna som vanlig text.

## Bootstrap

Jag använde Bootstrap för att göra webbsidan mer lättläst och ge den en tydligare layout.

I `base.html` lade jag till Bootstrap med en CDN-länk:

```html
<link
    href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
    rel="stylesheet"
>
```

Jag använde bland annat Bootstrap-klasser för formuläret, tabellen och sidans layout.

För att placera footern längst ner på sidan använde jag:

```html
<body class="d-flex flex-column min-vh-100">
```

`d-flex` aktiverar Flexbox.

`flex-column` placerar elementen vertikalt.

`min-vh-100` gör att sidan är minst lika hög som webbläsarfönstret.

Jag använde även:

```html
<main class="container mt-5 flex-grow-1">
```

`flex-grow-1` gör att huvudinnehållet tar upp det lediga utrymmet och skjuter ner footern.

## CSS och static

Jag skapade en `static`-mapp för att separera CSS från HTML.

I `static/style.css` skrev jag:

```css
table th {
    text-align: left !important;
}
```

`table th` väljer tabellens rubrikceller.

`text-align: left` gör att texten vänsterställs.

`!important` gör att regeln prioriteras framför andra vanliga CSS-regler.

Sedan kopplade jag CSS-filen till `base.html`:

```html
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
```

`url_for('static', ...)` gör att Flask hittar CSS-filen i mappen `static`.

## Footer och källhänvisning

Jag skapade en separat `footer.html` som visas längst ner på webbsidan.

I footern lade jag även till en länk till Elpriset Just Nu för att visa var informationen kommer ifrån.

Jag använde Bootstrap för att centrera texten och skapa avstånd runt footern.

## Kodkvalitet

Jag använde Ruff för att kontrollera och formatera Python-koden.

Från huvudmappen `Programmering2` körde jag:

```powershell
ruff check lektion4
```

Det kontrollerar om det finns problem i Python-koden.

Jag använde även:

```powershell
ruff format lektion4
```

Det formaterar koden enligt Ruffs regler.

Båda kommandona kördes utan problem.

## Starta programmet

Från huvudmappen `Programmering2` kan programmet startas med:

```powershell
flask --app "lektion4/app.py" run
```

För att aktivera automatisk omladdning under utvecklingen kan jag använda:

```powershell
flask --app "lektion4/app.py" run --debug
```

Öppna sedan adressen som Flask visar i terminalen:

```text
http://127.0.0.1:5000/
```

## Resultat

Webbsidan låter användaren:

- Välja år, månad och dag.
- Välja mellan elområdena SE1, SE2, SE3 och SE4.
- Hämta elpriser från Elpriset Just Nus API.
- Se elpriserna i en tabell med Bootstrap-styling.
- Få ett felmeddelande om datumet eller elområdet är ogiltigt.
- Få ett felmeddelande om API:et inte hittar några elpriser.

Jag har även delat upp projektet i separata HTML-filer och en CSS-fil för att hålla koden organiserad.

## Källa

Elpriserna hämtas från [Elpriset Just Nu](https://www.elprisetjustnu.se/).

API:et är öppet och kräver ingen API-nyckel.
