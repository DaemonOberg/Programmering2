from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        year = request.form.get("year")
        month = request.form.get("month")
        day = request.form.get("day")
        price_class = request.form.get("price_class")

        print(year, month, day, price_class)

    return render_template("index.html")
