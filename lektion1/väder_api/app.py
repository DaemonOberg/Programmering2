from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/api/weather/<city>")
def weather(city):
    return jsonify({"city": city, "temperature": "10°C", "condition": "Rainy"})
