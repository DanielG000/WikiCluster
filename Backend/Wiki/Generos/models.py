from flask import request, Response, jsonify
from flask_pymongo import PyMongo
import json
from bson import json_util
from bson.objectid import ObjectId

class ModeloGeneros:

    def __init__(self, app):
        self.__mongo = PyMongo(app)

    #Creación de Generos
    def crear_genero(self, request):
        resp = {}

        nombre = request.json['nombre']
        descripcion = request.json['descripcion']
        animes = request.json['animes']
        mangas = request.json['mangas']


        if nombre and descripcion and type(animes) is list and type(mangas) is list:

            generoId = self.existe_genero(nombre)
            
            if generoId is None:
                nuevo_genero = {'nombre':nombre, 'descripcion':descripcion,'animes':[],'mangas': []}

                generoId = self.__mongo.db.Generos.insert_one(nuevo_genero)

                listaAnimes = []
                if len(animes) >= 1:
                    listaAnimes = self.check_animes(animes, generoId=generoId.inserted_id, nombreGenero=nombre)
                    self.__mongo.db.Generos.update_one({'_id': ObjectId(generoId.inserted_id)},{'$set': {
                    'animes':listaAnimes
                    }} )

                listaMangas = []
                if len(mangas) >= 1:
                    listaMangas = self.check_mangas(mangas, generoId=generoId.inserted_id, nombreGenero=nombre)
                    self.__mongo.db.Generos.update_one({'_id': ObjectId(generoId.inserted_id)},{'$set': {
                    'mangas':listaMangas
                    }} )

                resp = {'body':{'_id':str(mangaId.inserted_id),'nombre':nombre,'descripcion': descripcion,'animes':listaAnimes,'mangas':listaMangas},'message':'Exitoso', 'status':200}
            else:
                resp= {'body':{'_id': str(mangaId['_id'])},'message': 'El genero ya existe', 'status':200}
        else:
            resp = {'message':'datos incompletos','status':406}

        resp = json_util.dumps(resp)
        return Response(resp, mimetype='application/json')

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

    #Retorna el manga y None en caso de no encontrar nada.
    def existe_manga(self, titulo):
        
        manga = None
        try:
            if type(titulo) is str:
                manga = self.__mongo.db.Mangas.find_one({'titulo':titulo})
            elif type(titulo) is dict:
                manga = self.__mongo.db.Mangas.find_one({'_id':titulo['_id'],'titulo':titulo['titulo']})
        except Exception as ex:
            return None
        
        return manga

    #Retorna el genero y None en caso de no encontrar ninguno.
    def existe_genero(self, nombre):
        
        genero = None
        try:
            genero = self.__mongo.db.Generos.find_one({'nombre':nombre})
        except Exception as ex:
            return None
        
        return genero


    #Funcion para establecer o crear referencias a la colección Animes
    def check_animes(self, animes, generoId, nombreGenero):
        listaAnimes = []

        for i in range(len(animes)):
            titulo = animes.pop()
            anime = self.existe_anime(titulo)
            if anime is None:
                nuevoAnime = {
                    'titulo':nombre,
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


    #Funcion para establecer o crear referencias a la colección Mangas
    def check_mangas(self, mangas, escritorId, nombreEscritor):
        listaMangas = []

        for i in range(len(mangas)):
            titulo = mangas.pop()
            manga = self.existe_manga(titulo)
            if manga is None:
                nuevoManga = {
                    'titulo':titulo,
                    'numero_capitulos':1,
                    'genero':[{'_id': str(generoId), 'nombre':nombreGenero}],
                    'escritor':None
                }
                manga = self.__mongo.db.Mangas.insert_one(nuevoManga)
                listaMangas.append({"_id":ObjectId(manga.inserted_id),"titulo":titulo})
            else:
                listaMangas.append({"_id":manga['_id'],"titulo":titulo})

        return listaMangas


    #Para obtener todos los generos
    def get_generos(self):
        genero = self.__mongo.db.Generos.find()
        genero = json_util.dumps(genero)
        return Response(genero, mimetype='application/json')


    #Para obtener un manga por medio de su ID
    def get_genero(self, id):
        try:
            genero = self.__mongo.db.Generos.find_one({'_id': ObjectId(id)})
            genero = json_util.dumps(genero)
        except Exception as ex:
            return jsonify({"status":404,"message":"Not Found"})

        return Response(genero, mimetype='application/json')

    #Eliminar un manga por medio de su ID
    def delete_genero(self, id):
        self.__mongo.db.Generos.delete_one({'_id': ObjectId(id)})
        resp = {'message':'delete '+ id + ' successfully', 'status':200}
        resp = json_util.dumps(resp)

        return Response(resp, mimetype='application/json')


    #Actualizar algun dato del manga
    def update_genero(self, id, request):
        resp = {}

        nombre = request.json['nombre']
        descripcion = request.json['descripcion']
        animes = request.json['animes']
        mangas = request.json['mangas']


        if nombre and descripcion and type(animes) is list and type(mangas) is list:

            self.__mongo.db.Generos.update_one({'_id': ObjectId(id)},{'$set': {
                'nombre':nombre,
                'descripcion':descripcion,
                'animes':[],
                'mangas':[]
                }} )

            listaAnimes = []
            if len(genero) >= 1:
                listaAnimes = self.check_animes(animes, generoId=id, nombreGenero=nombre)
                self.__mongo.db.Generos.update_one({'_id': ObjectId(id)},{'$set': {
                'animes':listaAnimes
                }} )

            listaMangas = []
            if len(genero) >= 1:
                listaMangas = self.check_mangas(mangas, generoId=id, nombreGenero=nombre)
                self.__mongo.db.Generos.update_one({'_id': ObjectId(id)},{'$set': {
                'mangas':listaMangas
                }} )
            
            resp = {'message':'update '+ id + ' successfully', 'status':200}
        else:
            resp = {'message':'datos incompletos','status':406}

        resp = json_util.dumps(resp)
        return Response(resp, mimetype='application/json')
