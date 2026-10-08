import requests
from flask import Flask, jsonify, render_template, request

# Importerar requests för att kunna skicka förfrågningar till externa API:er
# Importerar Flask för att skapa API:t och jsonify för att returnera JSON


# Skapar Flask-applikationen
app = Flask(__name__)


@app.route("/")
def index():

    city = request.args.get("city")
    resultat = None

    if city:
        resultat = get_weather(city)

    return render_template("index.html", city=city, resultat=resultat)


def get_weather(city):
    # URL till Open-Meteos Geocoding API
    geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"

    # Skickar med stadsnamnet som parameter
    params = {"name": city}

    # Skickar en GET-förfrågan till Geocoding API:t
    response = requests.get(geocoding_url, params=params)

    # Gör om JSON-svaret till Python-data
    data = response.json()

    # Hämtar det första resultatet från listan med städer
    first_result = data["results"][0]

    # Hämtar stadens koordinater
    latitude = first_result["latitude"]
    longitude = first_result["longitude"]

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


@app.route("/api/weather/<city>")
def weather(city):
    data = get_weather(city)
    return jsonify(data)
