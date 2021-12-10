from flask import Blueprint, request, jsonify
from marvel_api.helpers import token_required
from marvel_api.models import Person, db, person_schema, persons_schema

api = Blueprint('api', __name__, url_prefix='/api')




@api.route('/persons', methods=['POST'])
@token_required
def create_person(current_user_token):
    name = request.json['name']
    description = request.json['description']
    token = current_user_token.token

    print(f'TEST: {current_user_token.token}')

    person = person(name,description,user_token = token)

    db.session.add(person)
    db.session.commit()

    response = person_schema.dump(person)
    return jsonify(response)

@api.route('/persons', methods = ['GET'])
@token_required
def get_persons(current_user_token):
    owner = current_user_token.token
    persons = person.query.filter_by(user_token = owner).all()
    response = persons_schema.dump(persons)
    return jsonify(response)

@api.route('/persons/<id>', methods = ['GET'])
@token_required
def get_person(current_user_token, id):
    person = person.query.get(id)
    if person:
        print(f'Here is your person: {person.name}')
        response = person_schema.dump(person)
        return jsonify(response)
    else:
        return jsonify({'Error': 'That person does not exist!'})


@api.route('/persons/<id>', methods = ['POST', 'PUT'])
@token_required
def update_person(current_user_token, id):
    person = person.query.get(id)
    print(person)
    if person:
        person.name = request.json['name']
        person.description = request.json['description']
        person.user_token = current_user_token.token
        db.session.commit()

        response = person_schema.dump(person)
        return jsonify(response)
    else:
        return jsonify({'Error': 'That person does not exist!'})



@api.route('/persons/<id>', methods = ['DELETE'])
@token_required
def delete_person(current_user_token, id):
    person = person.query.get(id)
    if person:
        db.session.delete(person)
        db.session.commit()
        return jsonify({'Success': f'person ID #{person.id} has been deleted'})
    else:
        return jsonify({'Error': 'That person does not exist!'})
