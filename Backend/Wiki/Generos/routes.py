from flask import request, Response, jsonify
from .models import ModeloGeneros
from Wiki import app


dbm = ModeloGeneros(app)

@app.route('/Generos', methods=['POST'])
def crear_genero():
    results = dbm.crear_genero(request)

    return results


@app.route('/Generos', methods=['GET'])
def get_generos():
    results = dbm.get_generos()

    return results


@app.route('/Generos/<id>', methods=['GET'])
def get_genero(id):
    results = dbm.get_genero(id)

    return results


@app.route('/Generos/<id>', methods=['DELETE'])
def delete_genero(id):
    results = dbm.delete_genero(id)

    return results

@app.route('/Generos/<id>', methods=['PUT'])
def update_genero(id):
    results = dbm.update_genero(id,request)

    return results

@app.errorhandler(404)
def not_found(error=None):

    message = jsonify({
            'message': 'Recurso no encontrado ' +  request.url,
            'status': 404
            })

    return message


