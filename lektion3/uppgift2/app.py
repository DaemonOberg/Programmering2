import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/table")
def table():
    df = pd.DataFrame(
        {
            "Fruit": ["Apple", "Banana", "Lime"],
            "Color": ["Red/Green", "Yellow", "Green"],
        }
    )
    html = df.to_html(classes="table table-striped", index=False)
    return render_template("table.html", table=html)
