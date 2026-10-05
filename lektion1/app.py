from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return "Tjena världen!"

@app.route("/api/Tjena/<name>")
def tjena(name):
    return jsonify({"hälsning": f"Tjena {name}!"})