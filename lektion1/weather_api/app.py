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

    return jsonify(
        {"city": city, "temperature": f"{temperature}°C", "condition": condition}
    )
