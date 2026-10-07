# Importerar Pandas för att skapa och hantera tabeller/DataFrames
import pandas as pd

# Importerar Plotly Express för att skapa diagram
import plotly.express as px

# Importerar Flask och render_template
from flask import Flask, render_template

# Skapar Flask-applikationen
app = Flask(__name__)


# Skapar en route för startsidan
@app.route("/")
def table():
    # Skapar en DataFrame med information om frukterna
    df = pd.DataFrame(
        {
            "Fruits": ["Apple", "Banana", "Lime"],
            "Colors": ["Red/Green", "Yellow", "Green"],
            "Tastes": ["Sweet/Sour", "Sweet", "Sour"],
            "Favorite": [980000, 360000, 130000],
        }
    )

    # Skapar ett stapeldiagram med Fruits på x-axeln och Favorite på y-axeln
    fig = px.bar(df, x="Fruits", y="Favorite")

    # Gör om Plotly-diagrammet till HTML
    diagram = fig.to_html(full_html=False)

    # Gör om DataFrame-tabellen till HTML och lägger till Bootstrap-klasser
    # index=False gör att DataFrame-indexet inte visas
    html = df.to_html(classes="table table-striped", index=False)
    return render_template("table.html", table=html, diagram=diagram)
