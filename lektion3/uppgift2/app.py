import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def table():
    df = pd.DataFrame(
        {
            "Fruits": ["Apple", "Banana", "Lime"],
            "Colors": ["Red/Green", "Yellow", "Green"],
            "Tastes": ["Sweet/Sour", "Sweet", "Sour"],
        }
    )
    html = df.to_html(classes="table table-striped", index=False)
    return render_template("table.html", table=html)
