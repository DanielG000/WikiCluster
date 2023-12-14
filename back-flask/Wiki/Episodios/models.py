from flask import request, Response, jsonify
from flask_pymongo import PyMongo
import json
from bson import json_util
from bson.objectid import ObjectId

class ModeloEpisodios:

    def __init__(self, app):
        self.__mongo = PyMongo(app)

    #Creación de Episodio
    def crear_episodio(self, request):
        resp = {}

        numero = request.json['numero']
        nombre = request.json['nombre']
        duracion = request.json['duracion']
        anime = request.json['anime']
        personajes = request.json['personajes']


        if numero and nombre and duracion and (type(anime) is str or type(anime) is dict) and type(personajes) is list:

            episodioId = self.existe_episodio(numero, nombre, duracion)
            
            if episodioId is None:
                nuevo_episodio = {'numero':numero, 'nombre':nombre, 'duracion':duracion,'personajes':[]}

                episodioId = self.__mongo.db.Episodios.insert_one(nuevo_episodio)

                animeId = self.check_anime(anime, episodioId=episodioId.inserted_id, nombreEpisodio=nombre, numero=numero)
                self.__mongo.db.Episodios.update_one({'_id':ObjectId(episodioId.inserted_id)},{'$set':{'anime':animeId}})

                listaPersonajes = []
                if len(personajes) >= 1:
                    listaPersonajes = self.check_personajes(personajes, episodioId=episodioId.inserted_id, nombreEpisodio=nombre, numero=numero)
                    self.__mongo.db.Episodios.update_one({'_id': ObjectId(episodioId.inserted_id)},{'$set': {
                    'personajes':listaPersonajes
                    }} )

                resp = {'body':{'_id':str(episodioId.inserted_id), 'numero':numero, 'nombre':nombre, 'duración':duracion, 'personajes':listaPersonajes, 'anime':animeId},'message':'Exitoso', 'status':200}
            else:
                resp= {'body':{'_id': str(episodioId['_id'])},'message': 'El espisodio ya existe', 'status':200}
        else:
            resp = {'message':'datos incompletos','status':406}

        resp = json_util.dumps(resp)
        return Response(resp, mimetype='application/json')

    #Retorna el anime y None en caso de no encontrar nada.
    def existe_anime(self, titulo):
        
        anime = None
        try:
            if type(titulo) is str:
                anime = self.__mongo.db.Animes.find_one({'titulo':titulo})
        except Exception as ex:
            return None
        
        return anime


    #Retorna el episodio y None en caso de no encontrar ninguno.
    def existe_episodio(self, numero, nombre, duracion):
        
        episodio = None
        try:
            episodio = self.__mongo.db.Episodios.find_one({'numero':numero,'nombre':nombre, 'duracion':duracion})
        except Exception as ex:
            return None
        
        return episodio


    #Retorna el personaje y None en caso de no encontrar nada.
    def existe_personaje(self, nombre):
        
        personaje = None
        try:
            personaje = self.__mongo.db.Personajes.find_one({'nombre':nombre})
        except Exception as ex:
            return None
        
        return personaje

    #Funcion para establecer o crear referencias a la colección Mangas
    def check_personajes(self, personajes, episodioId, nombreEpisodio, numero):
        listaPersonajes = []

        for i in range(len(personajes)):
            nombre = personajes.pop()
            personaje = self.existe_personaje(nombre)
            if personaje is None:
                nuevoPersonaje = {
                    'nombre':nombre,
                    'tipo':None,
                    'sexo':None,
                    'animes':[],
                    'apariciones':[{
                        '_id':str(episodioId),
                        'nombre':nombreEpisodio,
                        'numero':numero
                        }],
                    'seiyuu':[]
                }
                personaje = self.__mongo.db.Personajes.insert_one(nuevoPersonaje)
                listaPersonajes.append({"_id":personaje.inserted_id,"nombre":nombre})
            else:
                listaPersonajes.append({"_id":personaje['_id'],"nombre":nombre})

        return listaPersonajes

    #Funcion para establecer o crear referencias a la colección Escritores
    def check_anime(self, titulo, episodioId, nombreEpisodio, numero):

        anime = self.existe_anime(titulo)

        if anime is None:
            if type(titulo) is dict:
                titulo = titulo['nombre']
            nuevo_anime = {
                'titulo': titulo,
                'lista_episodios':[{'_id': ObjectId(episodioId), 'nombre':nombreEpisodio, 'numero':numero}]
            }

            anime = self.__mongo.db.Animes.insert_one(nuevo_anime)
            anime = {'_id':anime.inserted_id, 'titulo':titulo}
        else:
            anime = {'_id':anime['_id'], 'titulo':anime['titulo']}

        return anime

    #Para obtener todos los generos
    def get_episodios(self):
        episodios = self.__mongo.db.Episodios.find()
        episodios = json_util.dumps(episodios)
        return Response(episodios, mimetype='application/json')


    #Para obtener un manga por medio de su ID
    def get_episodio(self, id):
        try:
            episodio = self.__mongo.db.Episodios.find_one({'_id': ObjectId(id)})
            episodio = json_util.dumps(episodio)
        except Exception as ex:
            return jsonify({"status":404,"message":"Not Found"})

        return Response(episodio, mimetype='application/json')

    #Eliminar un manga por medio de su ID
    def delete_episodio(self, id):
        self.__mongo.db.Episodios.delete_one({'_id': ObjectId(id)})
        resp = {'message':'delete '+ id + ' successfully', 'status':200}
        resp = json_util.dumps(resp)

        return Response(resp, mimetype='application/json')


    #Actualizar algun dato del manga
    def update_episodio(self, id, request):
        resp = {}

        numero = request.json['numero']
        nombre = request.json['nombre']
        duracion = request.json['duracion']
        anime = request.json['anime']
        personajes = request.json['personajes']


        if numero and nombre and duracion and (type(anime) is str or type(anime) is dict) and type(personajes) is list:

            self.__mongo.db.Episodios.update_one({'_id': ObjectId(id)},{'$set': {
                'numero':numero,
                'nombre':nombre,
                'duracion':duracion,
                'anime':None,
                'personajes':[]
                }} )


            animeId = self.check_anime(anime, episodioId=id, nombreEpisodio=nombre, numero=numero)
            self.__mongo.db.Episodios.update_one({'_id':ObjectId(id)},{'$set':{'anime':animeId}})

            listaPersonajes = []
            if len(personajes) >= 1:
                listaPersonajes = self.check_personajes(personajes, episodioId=id, nombreEpisodio=nombre, numero=numero)
                self.__mongo.db.Episodios.update_one({'_id': ObjectId(id)},{'$set': {
                'personajes':listaPersonajes
                }} )

            resp = {'message':'update '+ id + ' successfully', 'status':200}
        else:
            resp = {'message':'datos incompletos','status':406}

        resp = json_util.dumps(resp)
        return Response(resp, mimetype='application/json')
