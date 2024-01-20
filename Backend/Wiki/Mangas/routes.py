from flask import request, Response, jsonify
from .models import ModeloMangas
from Wiki import app


dbm = ModeloMangas(app)

@app.route('/Mangas', methods=['POST'])
def crear_manga():
    results = dbm.crear_manga(request)

    return results


@app.route('/Mangas', methods=['GET'])
def get_mangas():
    results = dbm.get_mangas()

    return results


@app.route('/Mangas/<id>', methods=['GET'])
def get_manga(id):
    results = dbm.get_manga(id)

    return results


@app.route('/Mangas/<id>', methods=['DELETE'])
def delete_manga(id):
    results = dbm.delete_manga(id)

    return results

@app.route('/Mangas/<id>', methods=['PUT'])
def update_manga(id):
    results = dbm.update_manga(id,request)

    return results

@app.errorhandler(404)
def not_found(error=None):

    message = jsonify({
            'message': 'Recurso no encontrado ' +  request.url,
            'status': 404
            })

    return message


