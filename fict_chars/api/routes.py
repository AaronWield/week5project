from operator import methodcaller
from flask import Blueprint, json, request, jsonify
from fict_chars.helpers import token_required
from fict_chars.models import Char, db, char_schema, chars_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'some_value': 52, 'another_value': 'Coding Temple'}

@api.route('/chars', methods=['POST'])
@token_required
def create_char(current_user_token):
    name = request.json['name']
    description = request.json['description']
    bio = request.json['bio']
    physical_appearance = request.json['physical_appearance']
    universe = request.json['universe']
    token = current_user_token.token
    char = Char(name,description,bio,physical_appearance,universe,user_token = token)

    db.session.add(char)
    db.session.commit()
    response = char_schema.dump(char)
    return jsonify(response)

@api.route('/chars', methods = ['GET'])
@token_required
def get_chars(current_user_token):
    owner = current_user_token.token
    chars = Char.query.filter_by(user_token = owner).all()
    response = chars_schema.dump(chars)
    return jsonify(response)

@api.route('/chars/<id>', methods = ['GET'])
@token_required
def get_char(current_user_token, id):
    char = Char.query.get(id)
    response = char_schema.dump(char)
    return jsonify(response)

@api.route('/chars/<id>', methods = ['POST', 'PUT'])
@token_required
def update_char(current_user_token, id):
    char = Char.query.get(id)
    print(char)
    if char:
        char.name = request.json['name']
        char.description = request.json['description']
        char.bio = request.json['bio']
        char.physical_appearance = request.json['physical_appearance']
        char.universe = request.json['universe']
        char.user_token = current_user_token.token
        db.session.commit()

        response = char_schema.dump(char)
        return jsonify(response)
    else:
        return jsonify({'Error': 'That character does not exist.'})

@api.route('/chars/<id>', methods = ['DELETE'])
@token_required
def delete_char(current_user_token, id):
    char = Char.query.get(id)
    if char:
        db.session.delete(char)
        db.session.commit()
        response = char_schema.dump(char)
        return jsonify({'Success': f'Character ID #{char.id} has been deleted'})
    else: 
        return jsonify({'Error': 'That character does not exist.'})
