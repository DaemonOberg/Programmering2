from flask import Flask, jsonify, render_template, request

# Skapar Flask-applikationen
app = Flask(__name__)


# Skapar en dictionary med användarnas ID och namn
users = {1: "Daemon", 2: "Emilia"}


# Skapar startsidan som förklarar hur användaren använder API:t
@app.route("/")
def index():
    return """Write in the URL /api/users/ and then your user id<br>
If you wanna add a new user write this in a second terminal<br>
curl.exe -X POST http://127.0.0.1:5000/api/users -H "Content-Type: application/json" --data-raw '{\\\"name\\\":\\\"Steve\\\"}'<br>
Steve is only an example, you can write whatever you want"""


# Skapar en GET-route som hämtar en användare med hjälp av användarens ID
@app.route("/api/users/<int:uid>")
def get_user(uid):
    # Kontrollerar om användarens ID finns i users
    if uid in users:
        # Returnerar användarens namn som JSON med statuskod 200 OK
        return jsonify({"name": users[uid]}), 200
    else:
        # Returnerar ett felmeddelande och statuskod 404 om användaren inte finns
        return jsonify({"Error": "User Not Found"}), 404


# Skapar en POST-route som används för att lägga till en ny användare
@app.route("/api/users", methods=["POST"])
def add_user():
    # Gör om JSON-datan från requesten till Python-data
    data = request.get_json()

    # Kontrollerar om "name" saknas i JSON-datan och returnerar 400 Bad Request
    if "name" not in data:
        return jsonify({"Error": "Name is required"}), 400

    # Skapar ett nytt användar-ID och sparar användarens namn
    users[len(users) + 1] = data["name"]

    # Returnerar den nya användaren som JSON med statuskod 201 Created
    return jsonify(data), 201


# Skapar en GET-route som hämtar sökord och sidnummer från query-parametrar
@app.route("/search")
def search():
    # Hämtar sökordet från "q", eller en tom sträng om det saknas
    q = request.args.get("q", "")

    # Hämtar sidnumret från "page", använder 1 som standard och gör om värdet till int
    page = request.args.get("page", 1, type=int)

    # Returnerar sökordet och sidnumret som JSON
    return jsonify({"search_word": q, "page": page})


# Hanterar 404-felet när en sida eller route inte hittas
@app.errorhandler(404)
def not_found(error):
    # Visar den egna 404-sidan och returnerar statuskod 404
    return render_template("404.html"), 404


# Hanterar 500-felet när ett internt serverfel uppstår
@app.errorhandler(500)
def server_error(error):
    # Returnerar ett felmeddelande som JSON med statuskod 500
    return jsonify({"Error": "Something went wrong!"}), 500
