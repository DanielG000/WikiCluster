from flask import request, Response, jsonify
from .models import ModeloAnimes
from Wiki import app


dbm = ModeloAnimes(app)

@app.route('/Animes', methods=['POST'])
def crear_anime():
    results = dbm.crear_anime(request)

    return results


@app.route('/Animes', methods=['GET'])
def get_animes():
    results = dbm.get_animes()

    return results


@app.route('/Animes/<id>', methods=['GET'])
def get_anime(id):
    results = dbm.get_anime(id)

    return results


@app.route('/Animes/<id>', methods=['DELETE'])
def delete_anime(id):
    results = dbm.delete_anime(id)

    return results

@app.route('/Animes/<id>', methods=['PUT'])
def update_anime(id):
    results = dbm.update_anime(id,request)

    return results

@app.errorhandler(404)
def not_found(error=None):

    message = jsonify({
            'message': 'Recurso no encontrado ' +  request.url,
            'status': 404
            })

    return message

