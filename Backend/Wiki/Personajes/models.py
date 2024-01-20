from flask import request, Response, jsonify
from flask_pymongo import PyMongo
import json
from bson import json_util
from bson.objectid import ObjectId

class ModeloPersonajes:

    def __init__(self, app):
        self.__mongo = PyMongo(app)

    # funcion de creacion de personaje
    def crear_personaje(self, request):
        resp = {}

        nombre = request.json['nombre']
        tipo = request.json['tipo']
        sexo = request.json['sexo']
        animes = request.json['animes']
        apariciones = request.json['apariciones']
        seiyuu = request.json['seiyuu']

        if nombre and tipo and sexo and type(animes) is list and type(apariciones) is list and seiyuu:

            personajeId = self.existe_personaje(nombre, tipo, sexo)
            
            if personajeId is None:
                nuevo_personaje = {'nombre':nombre,'tipo':tipo, 'sexo':sexo, 'animes':[],'apariciones':[],'seiyuu':[]}

                personajeId = self.__mongo.db.Personajes.insert_one(nuevo_personaje)


                listaAnimes = []
                if len(animes) >= 1:
                    listaAnimes = self.check_animes(animes, personajeId=personajeId.inserted_id, nombrePersonaje=nombre)
                    self.__mongo.db.Personajes.update_one({'_id': ObjectId(personajeId.inserted_id)},{'$set': {
                    'animes':listaAnimes
                    }} )
                    nuevo_personaje['animes'] = listaAnimes


                listaEpisodios = []
                if len(apariciones) >= 1:
                    listaEpisodios = self.check_episodios(apariciones, personajeId.inserted_id, nombrePersonaje=nombre)
                    self.__mongo.db.Personajes.update_one({'_id': ObjectId(personajeId.inserted_id)},{'$set': {
                    'apariciones':listaEpisodios
                    }} )
                    nuevo_personaje['apariciones'] = listaEpisodios

                listaSeiyuus = []
                if len(seiyuu) >= 1:
                    listaSeiyuus = self.check_seiyuus(seiyuu, personajeId.inserted_id, nombrePersonaje=nombre)
                    self.__mongo.db.Personajes.update_one({'_id': ObjectId(seiyuuId.inserted_id)},{'$set': {
                    'seiyuu':listaSeiyuus
                    }} )
                    nuevo_personaje['seiyuu'] = listaSeiyuus

                resp = {'body':{'_id':str(personajeId.inserted_id)}.update(nuevo_personaje),'message':'Exitoso', 'status':200}
            else:
                resp= {'body':{'_id': str(personajeId['_id'])},'message': 'El personaje ya existe', 'status':200}
        else:
            resp = {'message':'datos incompletos','status':406}

        resp = json_util.dumps(resp)
        return Response(resp, mimetype='application/json')


    #Retorna el personaje y None en caso de no encontrar nada.
    def existe_personaje(self, nombre, tipo, sexo):
        
        personaje = None
        try:
            personaje = self.__mongo.db.Personajes.find_one({'nombre':nombre, 'tipo':tipo, 'sexo':sexo})
        except Exception as ex:
            return None
        
        return personaje


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

    #Retorna el episodio y None en caso de no encontrar ninguno.
    def existe_episodio(self, episodioEntrada):
        
        numero, nombre= episodioEntrada['numero'],episodioEntrada['nombre']

        episodio = None
        try:
            episodio = self.__mongo.db.Episodios.find_one({'numero':numero,'nombre':nombre })
        except Exception as ex:
            return None
        
        return episodio


    #Retorna e seiyuu y None en caso de no encontrar nada.
    def existe_seiyuu(self, nombre):
        
        seiyuu = None
        try:
            seiyuu = self.__mongo.db.Seiyuus.find_one({'nombre':nombre})
        except Exception as ex:
            return None
        
        return seiyuu


    #Funcion para establecer o crear referencias a la colección Animes
    def check_animes(self, animes, personajeId, nombrePersonaje):
        listaAnimes = []

        for i in range(len(animes)):
            titulo = animes.pop()
            anime = self.existe_anime(titulo)
            if anime is None:
                nuevoAnime = {
                    'titulo':titulo,
                    'numero_episodios':1,
                    'lista_episodios':[],
                    'genero':[],
                    'personajes':[{'_id': str(personajeId), 'nombre':nombrePersonaje}],
                    'productor':None,
                    'manga':None
                }
                anime = self.__mongo.db.Animes.insert_one(nuevoAnime)
                listaAnimes.append({"_id":anime.inserted_id,"titulo":titulo})
            else:
                listaAnimes.append({"_id":anime['_id'],"titulo":titulo})

        return listaAnimes

    #Funcion para establecer o crear referencias a la colección Animes
    def check_episodios(self, episodios, personajeId, nombrePersonaje):
        listaEpisodios = []

        for i in range(len(episodios)):
            capitulo = episodios.pop()
            if type(capitulo) is dict:
                episodio = self.existe_anime(capitulo)
                if episodio is None:
                    nuevoEpisodio = {
                        'personajes':[{'_id': str(personajeId), 'nombre':nombrePersonaje}],
                        'nombre':capitulo['nombre'],
                        'numero':capitulo['numero']
                    }
    
                    nuevoEpisodio['anime'] = None
    
                    episodio = self.__mongo.db.Episodios.insert_one(nuevoEpisodio)
                    listaEpisodios.append({"_id":episodio.inserted_id,"numero":capitulo['numero'],'nombre':capitulo['nombre']})
                else:
                    listaEpisodios.append({"_id":episodio['_id'],"numero":capitulo['numero'],'nombre':capitulo['nombre']})
            else:
                continue

        return listaEpisodios

    #Funcion para establecer o crear referencias a la colección Animes
    def check_seiyuus(self, seiyuus, personajeId, nombrePersonaje):
        listaSeiyuus = []

        for i in range(len(seiyuus)):
            nombre = seiyuus.pop()
            seiyuu = self.existe_seiyuu(nombre)
            if seiyuu is None:
                nuevoSeiyuu = {
                    'nombre':nombre,
                    'personajes':[{'_id': str(personajeId), 'nombre':nombrePersonaje}]
                }
                seiyuu = self.__mongo.db.Seiyuus.insert_one(nuevoSeiyuu)
                listaSeiyuus.append({"_id":seiyuu.inserted_id,"nombre":nombre})
            else:
                listaSeiyuus.append({"_id":seiyuu['_id'],"nombre":nombre})

        return listaSeiyuus


    #Para obtener todos los escritores
    def get_personajes(self):
        personajes = self.__mongo.db.Personajes.find()
        personajes = json_util.dumps(personajes)
        return Response(personajes, mimetype='application/json')


    #Para obtener un escritor por medio de su ID
    def get_personaje(self, id):
        try:
            personaje = self.__mongo.db.Personajes.find_one({'_id': ObjectId(id)})
            personaje = json_util.dumps(personaje)
        except Exception as ex:
            return jsonify({"status":404,"message":"Not Found"})

        return Response(personaje, mimetype='application/json')

    #Eliminar un escritor por medio de su ID
    def delete_personaje(self, id):
        self.__mongo.db.Personajes.delete_one({'_id': ObjectId(id)})
        resp = {'message':'delete '+ id + ' successfully', 'status':200}
        resp = json_util.dumps(resp)

        return Response(resp, mimetype='application/json')


    #Actualizar algun dato del escritor
    def update_personaje(self, id, request):
        resp = {}

        nombre = request.json['nombre']
        tipo = request.json['tipo']
        sexo = request.json['sexo']
        animes = request.json['animes']
        apariciones = request.json['apariciones']
        seiyuu = request.json['seiyuu']


        if nombre and tipo and sexo and type(animes) is list and type(apariciones) is list and seiyuu:

            self.__mongo.db.Personajes.update_one({'_id': ObjectId(id)},{'$set': {
                'nombre':nombre,
                'tipo':tipo,
                'sexo':sexo
                }} )

            listaAnimes = []
            if len(animes) >= 1:
                listaAnimes = self.check_animes(animes, personajeId=id, nombrePersonaje=nombre)
                self.__mongo.db.Personajes.update_one({'_id': ObjectId(id)},{'$set': {
                'animes':listaAnimes
                }} )

            listaEpisodios = []
            if len(apariciones) >= 1:
                listaEpisodios = self.check_episodios(apariciones, id, nombrePersonaje=nombre)
                self.__mongo.db.Personajes.update_one({'_id': ObjectId(id)},{'$set': {
                'apariciones':listaEpisodios
                }} )

            listaSeiyuus = []
            if len(seiyuu) >= 1:
                listaSeiyuus = self.check_seiyuus(seiyuu, id, nombrePersonaje=nombre)
                self.__mongo.db.Personajes.update_one({'_id': ObjectId(id)},{'$set': {
                'seiyuu':listaSeiyuus
                }} )
            
            resp = {'message':'update '+ id + ' successfully', 'status':200}
        else:
            resp = {'message':'datos incompletos','status':406}

        
        resp = json_util.dumps(resp)
        return Response(resp, mimetype='application/json')
