# First API

Mitt första API byggt med Flask.

API:t har en startsida och en route som kan hälsa på användaren med ett namn.

## Starta API:t

Starta Flask-servern med:

```powershell
flask --app "lektion1/First_api/app.py" run
```

Servern körs på:

```text
http://127.0.0.1:5000
```

## Startsida

Gå till:

```text
http://127.0.0.1:5000/
```

Sidan returnerar:

```text
Tjena världen!
```

## Hälsning

Skriv ett namn efter `/api/Tjena/`:

```text
http://127.0.0.1:5000/api/Tjena/Steve
```

API:t returnerar svaret som JSON:

```json
{
    "hälsning": "Tjena Steve!"
}
```

Namnet i URL:en kan bytas ut mot valfritt namn.