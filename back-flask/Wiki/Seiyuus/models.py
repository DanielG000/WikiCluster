from flask import request, Response, jsonify
from flask_pymongo import PyMongo
import json
from bson import json_util
from bson.objectid import ObjectId

class ModeloSeiyuus:

    def __init__(self, app):
        self.__mongo = PyMongo(app)

    # funcion de creacion de seiyuu
    def crear_seiyuu(self, request):
        resp = {}

        nombre = request.json['nombre']
        personajes = request.json['personajes']

        if nombre and type(personajes) is list:

            seiyuuId = self.existe_seiyuu(nombre)
            
            if seiyuuId is None:
                nuevo_seiyuu = {'nombre':nombre,'personajes':[]}

                seiyuuId = self.__mongo.db.Seiyuus.insert_one(nuevo_seiyuu)

                listaPersonajes = []
                if len(personajes) >= 1:
                    listaPersonajes = self.check_personajes(personajes, seiyuuId=seiyuuId.inserted_id, nombreSeiyuu=nombre)
                    self.__mongo.db.Seiyuus.update_one({'_id': ObjectId(seiyuuId.inserted_id)},{'$set': {
                    'personajes':listaPersonajes
                    }} )

                resp = {'body':{'_id':str(seiyuuId.inserted_id),'nombre':nombre,'personajes':listaPersonajes},'message':'Exitoso', 'status':200}
            else:
                resp= {'body':{'_id': str(seiyuuId['_id'])},'message': 'El seiyuu ya existe', 'status':200}
        else:
            resp = {'message':'datos incompletos','status':406}

        resp = json_util.dumps(resp)
        return Response(resp, mimetype='application/json')

    #Retorna e seiyuu y None en caso de no encontrar nada.
    def existe_seiyuu(self, nombre):
        
        seiyuu = None
        try:
            seiyuu = self.__mongo.db.Seiyuus.find_one({'nombre':nombre})
        except Exception as ex:
            return None
        
        return seiyuu

    #Retorna el personaje y None en caso de no encontrar nada.
    def existe_personaje(self, nombre):
        
        personaje = None
        try:
            personaje = self.__mongo.db.Personajes.find_one({'nombre':nombre})
        except Exception as ex:
            return None
        
        return personaje

    #Funcion para establecer o crear referencias a la colección Mangas
    def check_personajes(self, personajes, seiyuuId, nombreSeiyuu):
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
                    'apariciones':[],
                    'seiyuu':[{
                    '_id':str(seiyuuId),
                    'nombre':nombreSeiyuu
                    }]
                }
                personaje = self.__mongo.db.Personajes.insert_one(nuevoPersonaje)
                listaPersonajes.append({"_id":personaje.inserted_id,"nombre":nombre})
            else:
                listaPersonajes.append({"_id":personaje['_id'],"nombre":nombre})

        return listaPersonajes


    #Para obtener todos los escritores
    def get_seiyuus(self):
        seiyuu = self.__mongo.db.Seiyuus.find()
        seiyuu = json_util.dumps(seiyuu)
        return Response(seiyuu, mimetype='application/json')


    #Para obtener un escritor por medio de su ID
    def get_seiyuu(self, id):
        try:
            seiyuu = self.__mongo.db.Seiyuus.find_one({'_id': ObjectId(id)})
            seiyuu = json_util.dumps(seiyuu)
        except Exception as ex:
            return jsonify({"status":404,"message":"Not Found"})

        return Response(seiyuu, mimetype='application/json')

    #Eliminar un escritor por medio de su ID
    def delete_seiyuu(self, id):
        self.__mongo.db.Escritores.delete_one({'_id': ObjectId(id)})
        resp = {'message':'delete '+ id + ' successfully', 'status':200}
        resp = json_util.dumps(resp)

        return Response(resp, mimetype='application/json')


    #Actualizar algun dato del escritor
    def update_seiyuu(self, id, request):
        resp = {}

        nombre = request.json['nombre']
        personajes = request.json['personajes']

        if nombre and type(personajes) is list:

            self.__mongo.db.Seiyuus.update_one({'_id': ObjectId(id)},{'$set': {
                'nombre':nombre,
                'personajes':[]
                }} )

            listaPersonajes = []
            if len(personajes) >= 1:
                listaPersonajes = self.check_mangas(personajes, seiyuuId=seiyuuId.inserted_id, nombreSeiyuu=nombre)
                self.__mongo.db.Seiyuus.update_one({'_id': ObjectId(seiyuuId.inserted_id)},{'$set': {
                'personajes':listaPersonajes
                }} )
            
            resp = {'message':'update '+ id + ' successfully', 'status':200}
        else:
            resp = {'message':'datos incompletos','status':406}

        
        resp = json_util.dumps(resp)
        return Response(resp, mimetype='application/json')
