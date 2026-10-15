# Importerar date för att kontrollera att datum är giltiga
from datetime import date

# Importerar biblioteken som behövs för API, tabeller och webbsidan
import pandas as pd
import requests
from flask import Flask, jsonify, render_template, request

# Skapar Flask-applikationen
app = Flask(__name__)


# Visar startsidan
@app.route("/")
def index():
    return render_template("index.html")


# Hanterar API-anrop och formulärdata
@app.route("/api", methods=["GET", "POST"])
def api():
    # Kontrollerar om användaren har skickat formuläret
    if request.method == "POST":
        # Hämtar användarens val från formuläret
        year = request.form.get("year")
        month = request.form.get("month")
        day = request.form.get("day")
        price_class = request.form.get("price_class")

        # Kontrollerar att elområdet är giltigt
        if price_class not in ["SE1", "SE2", "SE3", "SE4"]:
            return render_template("error.html"), 400

        # Kontrollerar att datumet existerar
        try:
            date(int(year), int(month), int(day))
        except (ValueError, TypeError):
            # Visar felsidan om datumet är ogiltigt
            return render_template("error.html"), 400

        # Ser till att dagen alltid har två siffror, exempelvis 01
        day = day.zfill(2)

        # Skapar URL:en till Elpriset Just Nus API
        url = f"https://www.elprisetjustnu.se/api/v1/prices/{year}/{month}-{day}_{price_class}.json"

        # Hämtar elpriserna från API:et
        response = requests.get(url, timeout=10)

        # Visar felsidan om det inte finns några elpriser
        if response.status_code == 404:
            return render_template("error.html"), 404

        # Omvandlar API-svaret från JSON till Python-data
        data = response.json()

        # Skapar en Pandas DataFrame av elpriserna
        df = pd.DataFrame(data)

        # Omvandlar DataFrame till en HTML-tabell med Bootstrap-styling
        html_table = df.to_html(
            classes="table table-striped table-bordered text-start", index=False
        )

        # Skickar tabellen till prices.html
        return render_template("prices.html", table=html_table)

    # Visar ett JSON-meddelande vid GET-anrop
    return jsonify({"message": "Mitt API fungerar!"})
