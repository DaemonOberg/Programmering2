import requests
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/api/weather/<city>")
def weather(city):
    geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city}
    response = requests.get(geocoding_url, params=params)
    data = response.json()
    first_result = data["results"][0]
    latitude = first_result["latitude"]
    longitude = first_result["longitude"]
    weather_url = "https://api.open-meteo.com/v1/forecast"
    params = {"latitude": latitude, "longitude": longitude, "current_weather": True}
    weather_response = requests.get(weather_url, params=params)
    weather_data = weather_response.json()
    temperature = weather_data["current_weather"]["temperature"]
    condition = weather_data["current_weather"]["weathercode"]
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
            condition = "Unknown"
    return jsonify(
        {"city": city, "temperature": f"{temperature}°C", "condition": condition}
    )
