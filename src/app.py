"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)
jackson_family = FamilyStructure("Jackson")

# Usuarios
initial_members = [
    {"first_name": "John", "age": 33, "lucky_numbers": [7, 13, 22]},
    {"first_name": "Jane", "age": 35, "lucky_numbers": [10, 14, 3]},
    {"first_name": "Jimmy", "age": 5, "lucky_numbers": [1]},
]

existing_names = {m["first_name"] for m in jackson_family.get_all_members()}
for m in initial_members:
    if m["first_name"] not in existing_names:
        jackson_family.add_member(m)
        existing_names.add(m["first_name"])



@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route("/")
def sitemap():
    return generate_sitemap(app)


#  GET /members -> LISTA
@app.route("/members", methods=["GET"])
def get_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200


#  GET /members/<id> -> OBJETO o 404
@app.route("/members/<int:member_id>", methods=["GET"])
def get_single_member(member_id):
    member = jackson_family.get_member(member_id)
    if member is None:
        return jsonify({"error": "Member not found"}), 404
    return jsonify(member), 200


#  POST /members -> crea miembro
@app.route("/members", methods=["POST"])
def create_member():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400

    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"error": "Invalid JSON body"}), 400

    first_name = body.get("first_name")
    age = body.get("age")
    lucky_numbers = body.get("lucky_numbers")

    if not isinstance(first_name, str) or not first_name.strip():
        return jsonify({"error": "first_name is required"}), 400
    if not isinstance(age, int) or age <= 0:
        return jsonify({"error": "age must be an int > 0"}), 400
    if not isinstance(lucky_numbers, list) or not all(isinstance(n, int) for n in lucky_numbers):
        return jsonify({"error": "lucky_numbers must be a list of integers"}), 400

    added = jackson_family.add_member({
        "first_name": first_name.strip(),
        "age": age,
        "lucky_numbers": lucky_numbers})

    if added is None:
        return jsonify({"error": "Invalid member data"}), 400

    return jsonify(added), 200


#  DELETE /members/<id> true o 404
@app.route("/members/<int:member_id>", methods=["DELETE"])
def remove_member(member_id):
    deleted = jackson_family.delete_member(member_id)
    if not deleted:
        return jsonify({"error": "Member not found"}), 404
    return jsonify({"done": True}), 200


if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=PORT, debug=True)
