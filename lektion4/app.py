import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/api", methods=["GET", "POST"])
def api():
    if request.method == "POST":
        year = request.form.get("year")
        month = request.form.get("month")
        day = request.form.get("day")
        price_class = request.form.get("price_class")
        day = day.zfill(2)
        url = f"https://www.elprisetjustnu.se/api/v1/prices/{year}/{month}-{day}_{price_class}.json"
        print(url)
        response = requests.get(url, timeout=10)
        print(response.status_code)
        data = response.json()
        print(data[0]["SEK_per_kWh"])
        print(response.status_code)
        return jsonify(
            {"year": year, "month": month, "day": day, "price_class": price_class}
        )
    return jsonify({"message": "Mitt API fungerar!"})
