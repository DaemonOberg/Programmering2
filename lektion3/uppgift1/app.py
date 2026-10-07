from flask import Flask, render_template

# Skapar Flask-applikationen
app = Flask(__name__)


# Skapar en route för startsidan
@app.route("/")
def index():
    # Hämtar och visar index.html från templates-mappen
    return render_template("index.html")
