# User API

Ett enkelt API byggt med Flask där man kan hämta och lägga till användare.

API:t innehåller även query-parametrar och felhantering för 404- och 500-fel.

## Installation

Skapa en virtual environment:

```powershell
python -m venv venv
```

Aktivera venv:

```powershell
.\venv\Scripts\Activate.ps1
```

Installera paketen från `requirements.txt`:

```powershell
pip install -r requirements.txt
```

## Starta API

Starta Flask-servern:

```powershell
flask --app .\lektion2\app.py run
```

Servern körs på:

```text
http://127.0.0.1:5000
```

## GET

Hämta en användare genom att skriva användarens ID:

```text
http://127.0.0.1:5000/api/users/1
```

Om användaren finns returneras `200 OK`.

Exempel:

```json
{
    "name": "Daemon"
}
```

## POST

Lägg till en ny användare med PowerShell:

```powershell
curl.exe -X POST http://127.0.0.1:5000/api/users -H "Content-Type: application/json" --data-raw '{\"name\":\"Steve\"}'
```

Om användaren skapas returneras `201 Created`.

Om `name` saknas returneras `400 Bad Request`.

## Query-parametrar

API:t har en `/search` route som använder query-parametrar.

Exempel:

```text
http://127.0.0.1:5000/search?q=python&page=2
```

`q` innehåller sökordet och `page` innehåller sidnumret.

API:t returnerar:

```json
{
    "search_word": "python",
    "page": 2
}
```

Om `q` saknas används en tom sträng som standard.

Om `page` saknas används `1` som standard.

## Felhantering

### 404 Not Found

Om användaren försöker gå till en route som inte finns visas en egen `404.html`-sida.

Exempel:

```text
http://127.0.0.1:5000/does-not-exist
```

Returnerar statuskod:

```text
404 Not Found
```

### 500 Internal Server Error

Om ett internt serverfel uppstår returnerar API:t:

```json
{
    "Error": "Something went wrong!"
}
```

med statuskoden:

```text
500 Internal Server Error
```