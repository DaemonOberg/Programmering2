# requests används för att skicka HTTP-förfrågningar till externa API:er
import requests

# Flask skapar webbapplikationen
# jsonify omvandlar Python-data till JSON-svar
# render_template visar HTML-filer med Jinja2
# request hämtar information från användarens HTTP-förfrågan
from flask import Flask, jsonify, render_template, request

# Skapar Flask-applikationen
app = Flask(__name__)


# Skapar startsidan för väderappen
@app.route("/")
def index():

    # Hämtar stadens namn från sökfältet via URL:en
    city = request.args.get("city")

    # Börjar utan någon väderinformation
    result = None

    # Hämtar vädret endast om användaren har angett en stad
    if city and city.isalpha():
        result = get_weather(city)

    # Skickar stadens namn och väderinformationen till HTML-sidan
    return render_template("index.html", city=city, result=result)


# Hämtar väderinformation för en stad från Open-Meteo
# Returnerar stad, temperatur och väderförhållande som en dictionary
def get_weather(city):
    # URL till Open-Meteos Geocoding API
    geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"

    # Skickar med stadsnamnet som parameter
    params = {"name": city}

    # Skickar en GET-förfrågan till Geocoding API:t
    response = requests.get(geocoding_url, params=params)

    # Gör om JSON-svaret till Python-data
    data = response.json()

    if "results" in data:
        first_result = data["results"][0]

        # Kontrollerar att stadens namn matchar sökningen
        if first_result["name"].casefold() != city.casefold():
            return None

        # Hämtar stadens koordinater
        latitude = first_result["latitude"]
        longitude = first_result["longitude"]

    else:
        return None

    # URL till Open-Meteos väder-API
    weather_url = "https://api.open-meteo.com/v1/forecast"

    # Skickar med koordinaterna och ber om aktuellt väder
    params = {"latitude": latitude, "longitude": longitude, "current_weather": True}

    # Skickar en GET-förfrågan till väder-API:t
    weather_response = requests.get(weather_url, params=params)

    # Gör om väder-API:ts JSON-svar till Python-data
    weather_data = weather_response.json()

    # Hämtar temperaturen och väderkoden från svaret
    temperature = weather_data["current_weather"]["temperature"]
    condition = weather_data["current_weather"]["weathercode"]

    # Översätter väderkoden till en text som är lättare att förstå
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
        case 48:
            condition = "Depositing rime fog"
        case 51:
            condition = "Light drizzle"
        case 53:
            condition = "Moderate drizzle"
        case 55:
            condition = "Dense drizzle"
        case 56:
            condition = "Light freezing drizzle"
        case 57:
            condition = "Dense freezing drizzle"
        case 61:
            condition = "Light rain"
        case 63:
            condition = "Moderate rain"
        case 65:
            condition = "Heavy rain"
        case 66:
            condition = "Light freezing rain"
        case 67:
            condition = "Heavy freezing rain"
        case 71:
            condition = "Light snow"
        case 73:
            condition = "Moderate snow"
        case 75:
            condition = "Heavy snow"
        case 77:
            condition = "Snow grains"
        case 80:
            condition = "Light rain showers"
        case 81:
            condition = "Moderate rain showers"
        case 82:
            condition = "Violent rain showers"
        case 85:
            condition = "Light snow showers"
        case 86:
            condition = "Heavy snow showers"
        case 95:
            condition = "Thunderstorm"
        case 96:
            condition = "Thunderstorm with slight hail"
        case 99:
            condition = "Thunderstorm with heavy hail"
        case _:
            # Används om väderkoden inte finns bland fallen ovan
            condition = "Unknown"

    return {"city": city, "temperature": f"{temperature}°C", "condition": condition}


# Skapar en API-route där användaren kan ange en stad i URL:en
@app.route("/api/weather/<city>")
def weather(city):

    # Anropar get_weather() och sparar väderinformationen
    data = get_weather(city)

    # Omvandlar väderinformationen till JSON och skickar tillbaka den
    return jsonify(data)
