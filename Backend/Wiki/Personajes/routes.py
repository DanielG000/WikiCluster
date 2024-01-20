from flask import request, Response, jsonify
from .models import ModeloPersonajes
from Wiki import app


dbm = ModeloPersonajes(app)

@app.route('/Personajes', methods=['POST'])
def crear_personaje():
    results = dbm.crear_personaje(request)

    return results


@app.route('/Personajes', methods=['GET'])
def get_personajes():
    results = dbm.get_personajes()

    return results


@app.route('/Personajes/<id>', methods=['GET'])
def get_personaje(id):
    results = dbm.get_personaje(id)

    return results


@app.route('/Personajes/<id>', methods=['DELETE'])
def delete_personaje(id):
    results = dbm.delete_personaje(id)

    return results

@app.route('/Personajes/<id>', methods=['PUT'])
def update_personaje(id):
    results = dbm.update_personaje(id,request)

    return results

@app.errorhandler(404)
def not_found(error=None):

    message = jsonify({
            'message': 'Recurso no encontrado ' +  request.url,
            'status': 404
            })

    return message

