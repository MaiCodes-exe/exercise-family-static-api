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
    response_body =members


    return jsonify(response_body), 200

###2nd method

@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    members= jackson_family.get_member(id)
    if members is not None:
        return jsonify(members), 200  
    else:       
        return "Member Not FOUND", 400

### 3) Add (POST) new member
@app.route('/member', methods=['POST'])
def add_member():
    members= request.json 
    if not members:
        return jsonify({"msj":"invalid input"}), 400
    jackson_family.add_member(members)       
    return jsonify({"msj":"Member added"}), 200


### 4) DELETE one member
@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    member = jackson_family.delete_member(member_id)
    if not member:
        return jsonify({"Msj":"Member has been deleted"}), 200
    return jsonify(member)


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
