from flask import request, Response, jsonify
from .models import ModelUsers
from Wiki import app


dbm = ModelUsers(app)

@app.route('/users', methods=['POST'])
def create_user():
    results = dbm.create_user(request)

    return results


@app.route('/users', methods=['GET'])
def get_users():
    results = dbm.get_users()

    return results


@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    results = dbm.get_user(id)

    return results


@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    results = dbm.delete_user(id)

    return results

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    results = dbm.update_user(id,request)

    return results

@app.errorhandler(404)
def not_found(error=None):

    message = jsonify({
            'message': 'Recurso no encontrado ' +  request.url,
            'status': 404
            })

    return message


