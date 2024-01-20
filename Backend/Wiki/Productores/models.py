from flask import request, Response, jsonify
from flask_pymongo import PyMongo
import json
from bson import json_util
from bson.objectid import ObjectId

class ModeloProductores:

    def __init__(self, app):
        self.__mongo = PyMongo(app)

    #Creación de Mangas
    def crear_productor(self, request):
        resp = {}

        nombre = request.json['nombre']
        animes = request.json['animes']


        if nombre and type(animes) is list:

            productorId = self.existe_productor(nombre)
            
            if productorId is None:
                nuevo_productor = {'nombre':nombre, 'animes':[]}

                productorId = self.__mongo.db.Productores.insert_one(nuevo_productor)

                listaAnimes = []
                if len(animes) >= 1:
                    listaAnimes = self.check_animes(animes, generoId=productorId.inserted_id, nombreGenero=nombre)
                    self.__mongo.db.Productores.update_one({'_id': ObjectId(productorId.inserted_id)},{'$set': {
                    'animes':listaAnimes
                    }} )

                resp = {'body':{'_id':str(productorId.inserted_id),'nombre':nombre,'animes': listaAnimes},'message':'Exitoso', 'status':200}
            else:
                resp= {'body':{'_id': str(productorId['_id'])},'message': 'El productor ya existe', 'status':200}
        else:
            resp = {'message':'datos incompletos','status':406}

        resp = json_util.dumps(resp)
        return Response(resp, mimetype='application/json')

    #Retorna el productor y None en caso de no encontrar nada.
    def existe_productor(self, nombre):
        
        productor = None
        try:
            productor = self.__mongo.db.Productores.find_one({'nombre':nombre})
        except Exception as ex:
            return None
        
        return productor

    #Retorna el anime y None en caso de no encontrar nada.
    def existe_anime(self, titulo):
        
        anime = None
        try:
            if type(titulo) is str:
                escritor = self.__mongo.db.Animes.find_one({'titulo':titulo})
            elif type(titulo) is dict:
                escritor = self.__mongo.db.Animes.find_one({'_id':titulo['_id'], 'titulo':titulo['titulo']})
        except Exception as ex:
            return None
        
        return anime

    #Funcion para establecer o crear referencias a la colección Animes
    def check_animes(self, animes, generoId, nombreGenero):
        listaAnimes = []

        for i in range(len(animes)):
            titulo = animes.pop()
            anime = self.existe_anime(titulo)
            if anime is None:
                nuevoAnime = {
                    'titulo':titulo,
                    'numero_episodios':1,
                    'lista_episodios':[],
                    'genero':[{'_id': str(generoId), 'nombre':nombreGenero}],
                    'personajes':[],
                    'productor':None,
                    'manga':None
                }
                anime = self.__mongo.db.Animes.insert_one(nuevoAnime)
                listaAnimes.append({"_id":anime.inserted_id,"titulo":titulo})
            else:
                listaAnimes.append({"_id":anime['_id'],"titulo":titulo})

        return listaAnimes


    #Para obtener todos los productores
    def get_productores(self):
        productores = self.__mongo.db.Productores.find()
        productores = json_util.dumps(productores)
        return Response(productores, mimetype='application/json')


    #Para obtener un productor por medio de su ID
    def get_productor(self, id):
        try:
            productor = self.__mongo.db.Productores.find_one({'_id': ObjectId(id)})
            productor = json_util.dumps(productor)
        except Exception as ex:
            return jsonify({"status":404,"message":"Not Found"})

        return Response(productor, mimetype='application/json')

    #Eliminar un productor por medio de su ID
    def delete_productor(self, id):
        self.__mongo.db.Productores.delete_one({'_id': ObjectId(id)})
        resp = {'message':'delete '+ id + ' successfully', 'status':200}
        resp = json_util.dumps(resp)

        return Response(resp, mimetype='application/json')


    #Actualizar algun dato del productor
    def update_productor(self, id, request):
        resp = {}


        nombre = request.json['nombre']
        animes = request.json['animes']


        if nombre and type(animes) is list:
            self.__mongo.db.Productores.update_one({'_id': ObjectId(id)},{'$set': {
                'nombre':nombre
                }} )

            listaAnimes = []
            if len(animes) >= 1:
                listaAnimes = self.check_animes(animes, generoId=id, nombreGenero=nombre)
                self.__mongo.db.Productores.update_one({'_id': ObjectId(id)},{'$set': {
                'animes':listaAnimes
                }} )
            
            resp = {'message':'update '+ id + ' successfully', 'status':200}
        else:
            resp = {'message':'datos incompletos','status':406}

        
        resp = json_util.dumps(resp)
        return Response(resp, mimetype='application/json')
