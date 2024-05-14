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

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

member_John = {"id":None,"first_name":"John", "age":33, "lucky_numbers":[7, 13, 22]}
member_Jane = {"id":None,"first_name":"Jane", "age":35, "lucky_numbers":[10, 14, 3]}
member_Jimmy = {"id":None,"first_name":"Jimmy", "age":5, "lucky_numbers":[1]}

jackson_family.add_member(member_John)
jackson_family.add_member(member_Jane)
jackson_family.add_member(member_Jimmy)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = members


    return jsonify(response_body), 200

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):

    member = jackson_family.get_member(member_id)
    response_body = member

    return jsonify(response_body), 200

@app.route('/member', methods=['POST'])
def add_member():
    if request.get_json()['id'] is None:
        id = None
    else:   
        id =request.get_json()['id']

     # first_name
    first_name =  request.get_json()['first_name']
    if not first_name:
        return jsonify({"error": "First name is required"}), 400
    
    # age
    age =  request.get_json()['age']
    if not age:
        return jsonify({"error": "Age is required"}), 400
    
    # lucky numbers
    lucky_numbers= request.get_json()['lucky_numbers']
    if not lucky_numbers:
        return jsonify({"error": "Lucky_numbers are required"}), 400
    
    member = {"id":id,"first_name":first_name, "age":age, "lucky_numbers":lucky_numbers}
    jackson_family.add_member(member)

    response_body = {
        "member": member,
        "msg": f"New member added to {jackson_family.last_name}",
    }

    return jsonify(response_body), 200



@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):

    delete_member = jackson_family.delete_member(member_id)

    if not delete_member:
        return jsonify({"error": "Member not found"}), 400

    response_body = delete_member

    return jsonify(response_body), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
