from flask import request, Response, jsonify
from .models import ModeloSeiyuus
from Wiki import app


dbm = ModeloSeiyuus(app)

@app.route('/Seiyuus', methods=['POST'])
def crear_seiyuu():
    results = dbm.crear_seiyuu(request)

    return results


@app.route('/Seiyuus', methods=['GET'])
def get_seiyuus():
    results = dbm.get_seiyuus()

    return results


@app.route('/Seiyuus/<id>', methods=['GET'])
def get_seiyuu(id):
    results = dbm.get_seiyuu(id)

    return results


@app.route('/Seiyuus/<id>', methods=['DELETE'])
def delete_seiyuu(id):
    results = dbm.delete_seiyuu(id)

    return results

@app.route('/Seiyuus/<id>', methods=['PUT'])
def update_seiyuu(id):
    results = dbm.update_seiyuu(id,request)

    return results

@app.errorhandler(404)
def not_found(error=None):

    message = jsonify({
            'message': 'Recurso no encontrado ' +  request.url,
            'status': 404
            })

    return message

