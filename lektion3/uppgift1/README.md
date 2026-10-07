# Uppgift 1 - Bootstrap och Jinja2

I denna uppgift skapades en statisk sida med Flask, Bootstrap och Jinja2.

Sidan använder `base.html` som grundmall och `index.html` som ärver från grundmallen med `extends` och `block`.

## Projektstruktur

```text
uppgift1/
│
├── templates/
│   ├── base.html
│   └── index.html
│
├── app.py
└── README.md
```

## Starta sidan

Starta Flask-servern från projektets rot:

```powershell
flask --app .\lektion3\uppgift1\app.py run
```

Servern körs på:

```text
http://127.0.0.1:5000
```

## Bootstrap

Bootstrap laddas i `base.html` från ett CDN.

```html
<link rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
```

Bootstrap används för sidans layout med färdiga CSS-klasser.

Exempel:

```html
<body class="container">
    <h1 class="mt-4">Mitt API</h1>
</body>
```

`container` används för sidans layout och `mt-4` lägger till marginal ovanför rubriken.

## Jinja2

`base.html` används som grundmall.

Den innehåller:

```html
{% block content %}
{% endblock %}
```

Det skapar ett område där andra templates kan lägga in eget innehåll.

`index.html` ärver från `base.html`:

```html
{% extends "base.html" %}

{% block content %}
    Welcome to lesson 3
{% endblock %}
```

`extends` gör att `index.html` använder strukturen från `base.html`.

## Flask

I `app.py` finns startsidans route:

```python
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")
```

`render_template()` hämtar och renderar `index.html` från `templates`-mappen.