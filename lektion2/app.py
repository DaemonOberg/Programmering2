from flask import Flask, jsonify, request, render_template

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

@app.route("/search")
def search():
    q = request.args.get("q", "")
    page = request.args.get("page", 1, type=int)
    return jsonify({"search_word": q, "page": page})

@app.errorhandler(404)
def inte_hittad(fel):
    return render_template("404.html"), 404


@app.errorhandler(500)
def serverfel(fel):
    return jsonify({"fel": "Något gick fel"}), 5