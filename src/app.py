"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)
jackson_family = FamilyStructure("Jackson")

# Initial family members
jackson_family.add_member({"first_name": "John", "age": 33, "lucky_numbers": [7, 13, 22]})
jackson_family.add_member({"first_name": "Jane", "age": 35, "lucky_numbers": [10, 14, 3]})
jackson_family.add_member({"first_name": "Jimmy", "age": 5, "lucky_numbers": [1]})


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route("/")
def sitemap():
    return generate_sitemap(app)


# 1) Get all family members
@app.route("/members", methods=["GET"])
def get_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200


# 2) Get a single family member
@app.route("/members/<int:member_id>", methods=["GET"])
def get_single_member(member_id):
    member = jackson_family.get_member(member_id)
    if member is None:
        return jsonify({"error": "Member not found"}), 400
    return jsonify(member), 200


# 3) Add a new family member
@app.route("/members", methods=["POST"])
def add_member():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"error": "Body must be JSON"}), 400

    added = jackson_family.add_member(body)
    if added is None:
        return jsonify({"error": "Invalid member data"}), 400

    return jsonify(added), 200


# 4) Delete a family member
@app.route("/members/<int:member_id>", methods=["DELETE"])
def delete_member(member_id):
    deleted = jackson_family.delete_member(member_id)
    if not deleted:
        return jsonify({"error": "Member not found"}), 400
    return jsonify({"done": True}), 200


if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=PORT, debug=True)
