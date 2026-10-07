# Lektion 3 - Uppgift 2

I den här uppgiften skapade jag en Flask-sida som visar en tabell med hjälp av Pandas och ett stapeldiagram med hjälp av Plotly.

Jag använde även Bootstrap för att styla tabellen och Jinja2 för att visa tabellen och diagrammet på HTML-sidan.

## Mappstruktur

```text
uppgift2/
│
├── templates/
│   ├── base.html
│   └── table.html
│
└── app.py
```

## Pandas

Jag importerade Pandas:

```python
import pandas as pd
```

Sedan skapade jag en DataFrame med information om olika frukter:

```python
df = pd.DataFrame(
    {
        "Fruits": ["Apple", "Banana", "Lime"],
        "Colors": ["Red/Green", "Yellow", "Green"],
        "Tastes": ["Sweet/Sour", "Sweet", "Sour"],
        "Favorite": [980000, 360000, 130000],
    }
)
```

En DataFrame lagrar information i rader och kolumner, ungefär som en tabell.

## Pandas till HTML

För att kunna visa DataFrame-tabellen på webbsidan gjorde jag om den till HTML:

```python
html = df.to_html(classes="table table-striped", index=False)
```

`classes="table table-striped"` använder Bootstrap-klasser för att styla tabellen.

`index=False` gör att Pandas index, till exempel `0`, `1` och `2`, inte visas i tabellen.

## Plotly

Jag importerade Plotly Express:

```python
import plotly.express as px
```

Sedan skapade jag ett stapeldiagram från samma DataFrame:

```python
fig = px.bar(df, x="Fruits", y="Favorite")
```

`Fruits` används på x-axeln och `Favorite` används på y-axeln.

Sedan gjorde jag om diagrammet till HTML:

```python
diagram = fig.to_html(full_html=False)
```

`full_html=False` gör att Plotly bara skapar HTML-koden som behövs för diagrammet istället för en helt ny HTML-sida.

## Flask

Startsidan skapas med:

```python
@app.route("/")
def table():
```

Sedan skickar Flask både tabellen och diagrammet till `table.html`:

```python
return render_template("table.html", table=html, diagram=diagram)
```

Det betyder att `table.html` får tillgång till variablerna `table` och `diagram`.

## Jinja2

I `table.html` använder jag:

```html
{% extends "base.html" %}

{% block content %}
    {{ table | safe }}
    {{ diagram | safe }}
{% endblock %}
```

`extends` gör att sidan använder `base.html` som grund.

`{{ table | safe }}` visar HTML-koden som skapades av Pandas.

`{{ diagram | safe }}` visar HTML-koden som skapades av Plotly.

`safe` gör att Jinja2 renderar innehållet som HTML istället för att visa HTML-koden som vanlig text.

## Bootstrap

I `base.html` laddas Bootstrap med:

```html
<link rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
```

Jag använder bland annat:

```html
<body class="container">
```

och Pandas-tabellen får Bootstrap-klasserna:

```text
table table-striped
```

Jag använde även CSS för att vänsterjustera rubrikerna i tabellen:

```css
th {
    text-align: left;
}
```

## Starta programmet

Från projektets huvudmapp kan programmet startas med:

```powershell
flask --app .\lektion3\uppgift2\app.py run
```

Öppna sedan adressen som Flask visar i terminalen.

## Resultat

Webbsidan visar:

- En Pandas-tabell med frukterna Apple, Banana och Lime.
- Information om färg, smak och Favorite.
- Ett Plotly-stapeldiagram som jämför frukternas Favorite-värden.
- Bootstrap-styling för tabellen och sidan.