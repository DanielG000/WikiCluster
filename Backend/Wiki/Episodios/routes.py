from flask import request, Response, jsonify
from .models import ModeloEpisodios
from Wiki import app


dbm = ModeloEpisodios(app)

@app.route('/Episodios', methods=['POST'])
def crear_episodio():
    results = dbm.crear_episodio(request)

    return results


@app.route('/Episodios', methods=['GET'])
def get_episodios():
    results = dbm.get_episodios()

    return results


@app.route('/Episodios/<id>', methods=['GET'])
def get_episodio(id):
    results = dbm.get_episodio(id)

    return results


@app.route('/Episodios/<id>', methods=['DELETE'])
def delete_episodio(id):
    results = dbm.delete_episodio(id)

    return results

@app.route('/Episodios/<id>', methods=['PUT'])
def update_episodio(id):
    results = dbm.update_episodio(id,request)

    return results

@app.errorhandler(404)
def not_found(error=None):

    message = jsonify({
            'message': 'Recurso no encontrado ' +  request.url,
            'status': 404
            })

    return message


