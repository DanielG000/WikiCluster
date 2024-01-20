from flask import request, Response, jsonify
from flask_pymongo import PyMongo
import json
from bson import json_util
from bson.objectid import ObjectId

class ModeloEscritores:

    def __init__(self, app):
        self.__mongo = PyMongo(app)

    # funcion de creacion de escritores
    def crear_escritor(self, request):
        resp = {}

        nombre = request.json['nombre']
        edad = request.json['edad']
        anio_nacimiento= request.json['año_nacimiento']
        mangas = request.json['mangas']

        if nombre and edad and anio_nacimiento and type(mangas) is list:

            escritorId = self.existe_escritor(nombre=nombre, anio_nacimiento=anio_nacimiento, mangas=mangas)
            
            if escritorId is None:
                nuevo_escritor = {'nombre':nombre,'edad':edad,'año_nacimiento':anio_nacimiento,'mangas':[]}

                escritorId = self.__mongo.db.Escritores.insert_one(nuevo_escritor)

                listaMangas = []
                if len(mangas) >= 1:
                    listaMangas = self.check_mangas(mangas, escritorId=escritorId.inserted_id, nombreEscritor=nombre)
                    self.__mongo.db.Escritores.update_one({'_id': ObjectId(escritorId.inserted_id)},{'$set': {
                    'mangas':listaMangas
                    }} )

                resp = {'body':{'_id':str(escritorId.inserted_id),'nombre':nombre,'edad': edad,'año_nacimiento':anio_nacimiento,'mangas':listaMangas},'message':'Exitoso', 'status':200}
            else:
                resp= {'body':{'_id': str(escritorId['_id'])},'message': 'El escritor ya existe', 'status':200}
        else:
            resp = {'message':'datos incompletos','status':406}

        resp = json_util.dumps(resp)
        return Response(resp, mimetype='application/json')

    #Retorna e escritor y None en caso de no encontrar nada.
    def existe_escritor(self, nombre, anio_nacimiento, mangas):
        
        escritor = None
        try:
            escritor = self.__mongo.db.Escritores.find_one({'nombre':nombre, 'año_nacimiento':anio_nacimiento})
        except Exception as ex:
            return None
        
        return escritor

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

    #Funcion para establecer o crear referencias a la colección Mangas
    def check_mangas(self, mangas, escritorId, nombreEscritor):
        listaMangas = []

        for i in range(len(mangas)):
            nombre = mangas.pop()
            manga = self.existe_manga(nombre)
            if manga is None:
                nuevoManga = {
                    'titulo':nombre,
                    'numero_capitulos':1,
                    'genero':[],
                    'escritor':{
                    '_id':str(escritorId),
                    'nombre':nombreEscritor
                    }
                }
                manga = self.__mongo.db.Mangas.insert_one(nuevoManga)
                listaMangas.append({"_id":manga.inserted_id,"titulo":nombre})
            else:
                listaMangas.append({"_id":manga['_id'],"titulo":nombre})

        return listaMangas


    #Para obtener todos los escritores
    def get_escritores(self):
        escritores = self.__mongo.db.Escritores.find()
        escritores = json_util.dumps(escritores)
        return Response(escritores, mimetype='application/json')


    #Para obtener un escritor por medio de su ID
    def get_escritor(self, id):
        try:
            escritor = self.__mongo.db.Escritores.find_one({'_id': ObjectId(id)})
            escritor = json_util.dumps(escritor)
        except Exception as ex:
            return jsonify({"status":404,"message":"Not Found"})

        return Response(escritor, mimetype='application/json')

    #Eliminar un escritor por medio de su ID
    def delete_escritor(self, id):
        self.__mongo.db.Escritores.delete_one({'_id': ObjectId(id)})
        resp = {'message':'delete '+ id + ' successfully', 'status':200}
        resp = json_util.dumps(resp)

        return Response(resp, mimetype='application/json')


    #Actualizar algun dato del escritor
    def update_escritor(self, id, request):
        resp = {}

        nombre = request.json['nombre']
        edad = request.json['edad']
        anio_nacimiento= request.json['año_nacimiento']
        mangas = request.json['mangas']


        if nombre and edad and anio_nacimiento and type(mangas) is list:
            self.__mongo.db.Escritores.update_one({'_id': ObjectId(id)},{'$set': {
                'nombre':nombre,
                'edad':edad,
                'año_nacimiento':anio_nacimiento,
                'mangas':[]
                }} )

            listaMangas = []
            if len(mangas) >= 1:
                listaMangas = self.check_mangas(mangas, escritorId=id, nombreEscritor=nombre)
                self.__mongo.db.Escritores.update_one({'_id': ObjectId(id)},{'$set': {
                'mangas':listaMangas
                }} )
            
            resp = {'message':'update '+ id + ' successfully', 'status':200}
        else:
            resp = {'message':'datos incompletos','status':406}

        
        resp = json_util.dumps(resp)
        return Response(resp, mimetype='application/json')
