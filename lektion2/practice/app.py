from flask import Flask, jsonify, request

app = Flask(__name__)
users = {1: "Daemon", 2: "Emilia"}


@app.route("/")
def index():
    return "Write in the URL /api/users/ and then your user id"


@app.route("/api/users/<int:uid>")
def get_user(uid):
    if uid in users:
        return jsonify({"name": users[uid]})
    else:
        return jsonify({"Error": "User Not Found"}), 404


@app.route("/api/users", methods=["POST"])
def add_user():
    data = request.get_json()
    users[len(users) + 1] = data["name"]
    return jsonify(data), 201
