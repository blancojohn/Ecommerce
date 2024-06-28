"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

@api.route('/register', methods = ['POST'])
def register_user():
    print(request.get_json())
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')

    if not email:
        return jsonify({"messagge": "Email es requerido"}), 400
    if not password:
        return jsonify({"messagge": "Password es requerido"}), 400
    
    found = User.query.filter_by(email=email).first()
    if found:
        return jsonify({"messagge":"Este email existe"}), 400
    
    user = User()
    user.name= name
    user.email = email
    #user.password = generate_password_hash(password)

    user.save()
    
    return jsonify({"success":"Registro satisfactorio, por favor iniciar sesión"}), 200