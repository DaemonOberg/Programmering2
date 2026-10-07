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

Om användaren inte finns returneras `404 Not Found`.

Exempel:

```text
http://127.0.0.1:5000/api/users/999
```

Svar:

```json
{
    "Error": "User Not Found"
}
```

## POST

Lägg till en ny användare med PowerShell:

```powershell
curl.exe -X POST http://127.0.0.1:5000/api/users -H "Content-Type: application/json" --data-raw '{\"name\":\"Steve\"}'
```

Om användaren skapas returneras `201 Created`.

Exempel på svar:

```json
{
    "name": "Steve"
}
```

Om `name` saknas i JSON-datan returneras `400 Bad Request`.

Exempel:

```json
{
    "Error": "Name is required"
}
```

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

Exempel:

```text
http://127.0.0.1:5000/search
```

Returnerar:

```json
{
    "search_word": "",
    "page": 1
}
```

## Felhantering

### 404 Not Found

API:t har en egen error handler för routes som inte finns.

Om användaren försöker gå till en route som inte finns används templaten:

```text
templates/404.html
```

Exempel:

```text
http://127.0.0.1:5000/does-not-exist
```

Sidan visar:

```text
404 Error: User Not Found
```

och returnerar statuskoden `404 Not Found`.

### 500 Internal Server Error

API:t har även en error handler för interna serverfel.

Om ett internt serverfel uppstår returneras:

```json
{
    "Error": "Something went wrong!"
}
```

med statuskoden `500 Internal Server Error`.

## Projektstruktur

```text
lektion2/
│
├── templates/
│   └── 404.html
│
├── app.py
└── README.md
```