# User API

Ett enkelt API byggt med Flask där man kan hämta och lägga till användare.

## Installation

Skapa en virtual environment:

```powershell
python -m venv venv
```

Aktivera venv:

```powershell
.\venv\Scripts\Activate.ps1
```

Installera paketen från requirements.txt:

```powershell
pip install -r requirements.txt
```

## Starta API

Starta Flask-servern:

```powershell
flask --app .\lektion2\app.py run
```

Servern körs på `http://127.0.0.1:5000`.

## GET

Hämta en användare genom att skriva användarens ID:

```text
http://127.0.0.1:5000/api/users/1
```

Om användaren finns returneras `200 OK`.

Om användaren inte finns returneras `404 Not Found`.

## POST

Lägg till en ny användare med PowerShell:

```powershell
curl.exe -X POST http://127.0.0.1:5000/api/users -H "Content-Type: application/json" --data-raw '{\"name\":\"Steve\"}'
```

Om användaren skapas returneras `201 Created`.

Om `name` saknas returneras `400 Bad Request`.