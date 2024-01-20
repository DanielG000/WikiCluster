from flask import request, Response, jsonify
from flask_pymongo import PyMongo
import json
from bson import json_util
from bson.objectid import ObjectId

class ModeloMangas:

    def __init__(self, app):
        self.__mongo = PyMongo(app)

    #Creación de Mangas
    def crear_manga(self, request):
        resp = {}

        titulo = request.json['titulo']
        numero_capitulos = request.json['numero_capitulos']
        genero= request.json['genero']
        escritor = request.json['escritor']


        if titulo and numero_capitulos and type(genero) is list and (type(escritor) is dict or type(escritor) is str):

            mangaId = self.existe_manga(titulo=titulo)
            
            if mangaId is None:
                nuevo_manga = {'titulo':titulo, 'numero_capitulos':numero_capitulos,'genero':[],'escritor': None}

                mangaId = self.__mongo.db.Mangas.insert_one(nuevo_manga)

                #Verifica si es existe o crea el escritor y actualiza el manga.
                escritor = self.check_escritor(nombre=escritor, mangaId=mangaId.inserted_id, tituloManga=titulo)
                self.__mongo.db.Mangas.update_one({'_id': ObjectId(mangaId.inserted_id)},{'$set':{'escritor':escritor}})

                listaGeneros = []
                if len(genero) >= 1:
                    listaGeneros = self.check_generos(genero, mangaId=mangaId.inserted_id, tituloManga=titulo)
                    self.__mongo.db.Mangas.update_one({'_id': ObjectId(mangaId.inserted_id)},{'$set': {
                    'genero':listaGeneros
                    }} )

                resp = {'body':{'_id':str(mangaId.inserted_id),'titulo':titulo,'numero_capitulos': numero_capitulos,'genero':listaGeneros,'escritor':escritor},'message':'Exitoso', 'status':200}
            else:
                resp= {'body':{'_id': str(mangaId['_id'])},'message': 'El manga ya existe', 'status':200}
        else:
            resp = {'message':'datos incompletos','status':406}

        resp = json_util.dumps(resp)
        return Response(resp, mimetype='application/json')

    #Retorna el escritor y None en caso de no encontrar nada.
    def existe_escritor(self, nombre):
        
        escritor = None
        try:
            if type(nombre) is str:
                escritor = self.__mongo.db.Escritores.find_one({'nombre':nombre})
            elif type(nombre) is dict:
                escritor = self.__mongo.db.Escritores.find_one(nombre)
        except Exception as ex:
            return None
        
        return escritor

    #Retorna el manga y None en caso de no encontrar ninguno.
    def existe_manga(self, titulo):
        
        manga = None
        try:
            manga = self.__mongo.db.Mangas.find_one({'titulo':titulo})
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


    #Funcion para establecer o crear referencias a la colección Escritores
    def check_escritor(self, nombre, mangaId, tituloManga):

        escritor = self.existe_escritor(nombre=nombre)

        if escritor is None:
            if type(nombre) is dict:
                nombre = nombre['nombre']
            nuevo_escritor = {
                'nombre': nombre,
                'edad': None,
                'año_nacimiento': None,
                'mangas':[{'_id': ObjectId(mangaId), 'titulo':tituloManga}]
            }

            escritor = self.__mongo.db.Escritores.insert_one(nuevo_escritor)
            escritor = {'_id':ObjectId(escritor.inserted_id), 'nombre':nombre}
        else:
            escritor = {'_id':escritor['_id'], 'nombre':escritor['nombre']}

        return escritor


    #Funcion para establecer o crear referencias a la colección Generos
    def check_generos(self, generos, mangaId, tituloManga):
        listaGeneros = []

        for i in range(len(generos)):
            nombre = generos.pop()
            genero = self.existe_genero(nombre)
            if genero is None:
                nuevoGenero = {
                    'nombre':nombre,
                    'descripcion':"",
                    'animes':[],
                    'mangas':[{
                    '_id':str(mangaId),
                    'titulo':tituloManga
                    }]
                }
                genero = self.__mongo.db.Generos.insert_one(nuevoGenero)
                listaGeneros.append({"_id":genero.inserted_id,"titulo":nombre})
            else:
                mangas = genero['mangas']
                nuevo = {'_id':str(mangaId), 'titulo':tituloManga}
                if not nuevo in mangas:
                    mangas.append(nuevo)
                self.__mongo.db.Generos.update_one({'_id':genero['_id']},{'$set':{'mangas':mangas}})
                listaGeneros.append({"_id":genero['_id'],"nombre":nombre})

        return listaGeneros


    #Para obtener todos los mangas
    def get_mangas(self):
        mangas = self.__mongo.db.Mangas.find()
        mangas = json_util.dumps(mangas)
        return Response(mangas, mimetype='application/json')


    #Para obtener un manga por medio de su ID
    def get_manga(self, id):
        try:
            manga = self.__mongo.db.Mangas.find_one({'_id': ObjectId(id)})
            manga = json_util.dumps(manga)
        except Exception as ex:
            return jsonify({"status":404,"message":"Not Found"})

        return Response(manga, mimetype='application/json')

    #Eliminar un manga por medio de su ID
    def delete_manga(self, id):
        self.__mongo.db.Mangas.delete_one({'_id': ObjectId(id)})
        resp = {'message':'delete '+ id + ' successfully', 'status':200}
        resp = json_util.dumps(resp)

        return Response(resp, mimetype='application/json')


    #Actualizar algun dato del manga
    def update_manga(self, id, request):
        resp = {}

        titulo = request.json['titulo']
        numero_capitulos = request.json['numero_capitulos']
        genero= request.json['genero']
        escritor = request.json['escritor']



        if titulo and numero_capitulos and type(genero) is list and (type(escritor) is dict or type(escritor) is str):
            escritor = self.check_escritor(nombre=escritor, mangaId=id, tituloManga=titulo)
            self.__mongo.db.Mangas.update_one({'_id': ObjectId(id)},{'$set': {
                'titulo':titulo,
                'numero_capitulos':numero_capitulos,
                'genero':[],
                'escritor':escritor
                }} )

            listaGeneros = []
            if len(genero) >= 1:
                listaGeneros = self.check_generos(genero, mangaId=id, tituloManga=titulo)
                self.__mongo.db.Mangas.update_one({'_id': ObjectId(id)},{'$set': {
                'genero':listaGeneros
                }} )
            
            resp = {'message':'update '+ id + ' successfully', 'status':200}
        else:
            resp = {'message':'datos incompletos','status':406}

        
        resp = json_util.dumps(resp)
        return Response(resp, mimetype='application/json')
