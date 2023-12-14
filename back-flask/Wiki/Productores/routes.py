from flask import request, Response, jsonify
from .models import ModeloProductores
from Wiki import app


dbm = ModeloProductores(app)

@app.route('/Productores', methods=['POST'])
def crear_productor():
    results = dbm.crear_productor(request)

    return results


@app.route('/Productores', methods=['GET'])
def get_productores():
    results = dbm.get_productores()

    return results


@app.route('/Productores/<id>', methods=['GET'])
def get_productor(id):
    results = dbm.get_productor(id)

    return results


@app.route('/Productores/<id>', methods=['DELETE'])
def delete_productor(id):
    results = dbm.delete_productor(id)

    return results

@app.route('/Productores/<id>', methods=['PUT'])
def update_productor(id):
    results = dbm.update_productor(id,request)

    return results

@app.errorhandler(404)
def not_found(error=None):

    message = jsonify({
            'message': 'Recurso no encontrado ' +  request.url,
            'status': 404
            })

    return message


