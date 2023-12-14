from flask import request, Response, jsonify
from .models import ModeloEscritores
from Wiki import app


dbm = ModeloEscritores(app)

@app.route('/Escritores', methods=['POST'])
def crear_escritor():
    results = dbm.crear_escritor(request)

    return results


@app.route('/Escritores', methods=['GET'])
def get_escritores():
    results = dbm.get_escritores()

    return results


@app.route('/Escritores/<id>', methods=['GET'])
def get_escritor(id):
    results = dbm.get_escritor(id)

    return results


@app.route('/Escritores/<id>', methods=['DELETE'])
def delete_escritor(id):
    results = dbm.delete_escritor(id)

    return results

@app.route('/Escritores/<id>', methods=['PUT'])
def update_escritor(id):
    results = dbm.update_escritor(id,request)

    return results

@app.errorhandler(404)
def not_found(error=None):

    message = jsonify({
            'message': 'Recurso no encontrado ' +  request.url,
            'status': 404
            })

    return message

