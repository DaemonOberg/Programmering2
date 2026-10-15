from datetime import date

import pandas as pd
import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api", methods=["GET", "POST"])
def api():
    if request.method == "POST":
        year = request.form.get("year")
        month = request.form.get("month")
        day = request.form.get("day")
        price_class = request.form.get("price_class")

        if price_class not in ["SE1", "SE2", "SE3", "SE4"]:
            return render_template("error.html"), 400

        try:
            date(int(year), int(month), int(day))
        except (ValueError, TypeError):
            return render_template("error.html"), 400

        day = day.zfill(2)
        url = f"https://www.elprisetjustnu.se/api/v1/prices/{year}/{month}-{day}_{price_class}.json"
        response = requests.get(url, timeout=10)

        if response.status_code == 404:
            return render_template("error.html"), 404

        data = response.json()
        df = pd.DataFrame(data)
        html_table = df.to_html(
            classes="table table-striped table-bordered text-start", index=False
        )
        return render_template("prices.html", table=html_table)
    return jsonify({"message": "Mitt API fungerar!"})
