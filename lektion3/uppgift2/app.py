import pandas as pd
import plotly.express as px
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def table():
    df = pd.DataFrame(
        {
            "Fruits": ["Apple", "Banana", "Lime"],
            "Colors": ["Red/Green", "Yellow", "Green"],
            "Tastes": ["Sweet/Sour", "Sweet", "Sour"],
            "Favorite": [980000, 360000, 130000],
        }
    )
    fig = px.bar(df, x="Fruits", y="Favorite")
    diagram = fig.to_html(full_html=False)
    html = df.to_html(classes="table table-striped", index=False)
    return render_template("table.html", table=html, diagram=diagram)
