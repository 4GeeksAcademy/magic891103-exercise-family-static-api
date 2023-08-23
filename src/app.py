"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the Jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors as JSON objects
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Generate a sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_members():
    all_members = jackson_family.get_all_members()
    return jsonify(all_members)

@app.route('/members', methods=['POST'])
def insert_member():
    # This is how you can use the Family data structure by calling its methods
    request_body = request.json
    print(request_body)
    jackson_family.add_member(request_body)
    return jsonify("Everything went great"), 200

@app.route('/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    # This is how you can use the Family data structure by calling its methods
    single_member = jackson_family.get_member(member_id)
    if single_member:
        return jsonify(single_member), 200
    else:
        return jsonify({"error": "The family member has not been found or their skin color changed after many surgeries/genetic anomalies"}), 404

@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    # This is how you can use the Family data structure by calling its methods
    jackson_family.delete_member(member_id)
    return jsonify("Member deleted"), 200

# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)