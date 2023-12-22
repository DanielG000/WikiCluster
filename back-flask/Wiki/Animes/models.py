from flask import request, Response, jsonify
from flask_pymongo import PyMongo
import json
from bson import json_util
from bson.objectid import ObjectId

class ModeloAnimes:

    def __init__(self, app):
        self.__mongo = PyMongo(app)

    # funcion de creacion de personaje
    def crear_anime(self, request):
        resp = {}

        titulo = request.json['titulo']
        numero_episodios = request.json['numero_episodios']
        lista_episodios = request.json['lista_episodios']
        genero = request.json['genero']
        personajes = request.json['personajes']
        productor = request.json['productor']
        manga = request.json['manga']

        if titulo and numero_episodios and type(lista_episodios) is list and type(genero) is list and type(personajes) is list and productor and manga:

            animeId = self.existe_anime(titulo)
            
            if animeId is None:
                nuevo_anime = {'titulo':titulo,'numero_episodios':numero_episodios, 'lista_episodios':[],'genero':[], 'personajes':[],'productor':None,'manga':None}


                animeId = self.__mongo.db.Animes.insert_one(nuevo_anime)

                listaEpisodios = []
                if len(lista_episodios) >= 1:
                    listaEpisodios = self.check_episodios(lista_episodios, animeId.inserted_id, tituloAnime=titulo)
                    self.__mongo.db.Animes.update_one({'_id': ObjectId(animeId.inserted_id)},{'$set': {
                    'lista_episodios':listaEpisodios
                    }} )
                    nuevo_anime['lista_episodios'] = listaEpisodios

                listaGeneros = []
                if len(genero) >= 1:
                    listaGeneros = self.check_generos(genero, animeId=animeId.inserted_id, tituloAnime=titulo)
                    self.__mongo.db.Animes.update_one({'_id': ObjectId(animeId.inserted_id)},{'$set': {
                    'genero':listaGeneros
                    }} )

                listaPersonajes = []
                if len(personajes) >= 1:
                    listaPersonajes = self.check_personajes(personajes, animeId=animeId.inserted_id, tituloAnime=titulo)
                    self.__mongo.db.Animes.update_one({'_id': ObjectId(animeId.inserted_id)},{'$set': {
                    'personajes':listaPersonajes
                    }} )

                productorId = self.check_productor(productor, animeId.inserted_id, titulo)
                self.__mongo.db.Animes.update_one({'_id': ObjectId(animeId.inserted_id)},{'$set': {'productor':productorId}} )

                mangaId = self.check_manga(manga, animeId.inserted_id, titulo)
                self.__mongo.db.Animes.update_one({'_id': ObjectId(animeId.inserted_id)},{'$set': {'manga':mangaId}} )

                resp = {'body':{'_id':str(animeId.inserted_id), 'titulo':titulo,'numero_episodios':numero_episodios, 'lista_episodios':listaEpisodios,'genero':listaGeneros, 'personajes':listaPersonajes,'productor':productorId,'manga':mangaId},'message':'Exitoso', 'status':200}
            else:
                resp= {'body':{'_id': str(animeId['_id'])},'message': 'El Anime ya existe', 'status':200}
        else:
            resp = {'message':'datos incompletos','status':406}

        resp = json_util.dumps(resp)
        return Response(resp, mimetype='application/json')


    

    #Retorna el personaje y None en caso de no encontrar nada.
    def existe_personaje(self, nombre):
        
        personaje = None
        try:
            personaje = self.__mongo.db.Personajes.find_one({'nombre':nombre})
        except Exception as ex:
            return None
        
        return personaje


    #Retorna el anime y None en caso de no encontrar nada.
    def existe_anime(self, titulo):
        
        anime = None
        try:
            if type(titulo) is str:
                anime = self.__mongo.db.Animes.find_one({'titulo':titulo})
            elif type(titulo) is dict:
                anime = self.__mongo.db.Animes.find_one({'_id':titulo['_id'], 'titulo':titulo['titulo']})
        except Exception as ex:
            return None
        
        return anime

    #Retorna el genero y None en caso de no encontrar ninguno.
    def existe_genero(self, nombre):
        
        genero = None
        try:
            genero = self.__mongo.db.Generos.find_one({'nombre':nombre})
        except Exception as ex:
            return None
        
        return genero

    #Retorna el episodio y None en caso de no encontrar ninguno.
    def existe_episodio(self, capitulo):
        
        numero, nombre = capitulo['numero'],capitulo['nombre']

        episodio = None
        try:
            episodio = self.__mongo.db.Episodios.find_one({'numero':numero,'nombre':nombre})
        except Exception as ex:
            return None
        
        return episodio

    #Retorna el productor y None en caso de no encontrar nada.
    def existe_productor(self, nombre):
        
        productor = None
        try:
            productor = self.__mongo.db.Productores.find_one({'nombre':nombre})
        except Exception as ex:
            return None
        
        return productor

    #Retorna el manga y None en caso de no encontrar ninguno.
    def existe_manga(self, titulo):
        
        manga = None
        try:
            manga = self.__mongo.db.Mangas.find_one({'titulo':titulo})
        except Exception as ex:
            return None
        
        return manga


    #Funcion para establecer o crear referencias a la colección Generos
    def check_generos(self, generos, animeId, tituloAnime):
        listaGeneros = []

        for i in range(len(generos)):
            nombre = generos.pop()
            genero = self.existe_genero(nombre)
            if genero is None:
                nuevoGenero = {
                    'nombre':nombre,
                    'descripcion':"",
                    'animes':[{'_id':ObjectId(animeId), 'titulo':tituloAnime}],
                    'mangas':[]
                }
                genero = self.__mongo.db.Generos.insert_one(nuevoGenero)
                listaGeneros.append({"_id":genero.inserted_id,"titulo":nombre})
            else:
                animes = genero['animes']
                nuevo = {'_id':ObjectId(animeId), 'titulo':tituloAnime}
                if not nuevo in animes:
                    animes.append(nuevo)
                self.__mongo.db.Generos.update_one({'_id':genero['_id']},{'$set':{'animes':animes}})
                listaGeneros.append({"_id":genero['_id'],"nombre":nombre})

        return listaGeneros

    #Funcion para establecer o crear referencias a la colección Animes
    def check_episodios(self, episodios, animeId, tituloAnime):
        listaEpisodios = []

        for i in range(len(episodios)):
            capitulo = episodios.pop()
            if type(capitulo) is dict:
                episodio = self.existe_anime(capitulo)
                if episodio is None:
                    nuevoEpisodio = {
                        'numero':capitulo['numero'],
                        'nombre':capitulo['nombre'],
                        'anime':{'_id':ObjectId(animeId),'titulo':tituloAnime}
                    }
    
                    episodio = self.__mongo.db.Episodios.insert_one(nuevoEpisodio)
                    listaEpisodios.append({"_id":episodio.inserted_id,"numero":capitulo['numero'],'nombre':capitulo['nombre']})
                else:
                    listaEpisodios.append({"_id":episodio['_id'],"numero":capitulo['numero'],'nombre':capitulo['nombre']})
            else:
                continue

        return listaEpisodios

    #Funcion para establecer o crear referencias a la colección Personajes
    def check_personajes(self, personajes, animeId, tituloAnime):
        listaPersonajes = []

        for i in range(len(personajes)):
            nombre = personajes.pop()
            personaje = self.existe_personaje(nombre)
            if personaje is None:
                nuevoPersonaje = {
                    'nombre':nombre,
                    'tipo':None,
                    'sexo':None,
                    'animes':[{
                    '_id':ObjectId(animeId),
                    'titulo':tituloAnime
                    }],
                    'apariciones':[],
                    'seiyuu':[]
                }
                personaje = self.__mongo.db.Personajes.insert_one(nuevoPersonaje)
                listaPersonajes.append({"_id":personaje.inserted_id,"nombre":nombre})
            else:
                animes = personaje['animes']
                nuevo = {'_id':ObjectId(animeId), 'titulo':tituloAnime}
                if not nuevo in animes:
                    animes.append(nuevo)
                self.__mongo.db.Personajes.update_one({'_id':personaje['_id']},{'$set':{'animes':animes}})
                listaPersonajes.append({"_id":personaje['_id'],"nombre":nombre})

        return listaPersonajes

    #Funcion para establecer o crear referencias a la colección Productores
    def check_productor(self, nombre, animeId, tituloAnime):

        productor = self.existe_productor(nombre)

        if productor is None:
            if type(nombre) is dict:
                nombre = nombre['nombre']
            nuevo_productor = {
                'nombre': nombre,
                'animes':[{'_id':ObjectId(animeId), 'nombre':tituloAnime}]
            }

            productor = self.__mongo.db.Productores.insert_one(nuevo_productor)
            productor = {'_id':ObjectId(productor.inserted_id), 'nombre':nombre}
        else:
            animes = productor['animes']
            nuevo = {'_id':ObjectId(animeId), 'titulo':tituloAnime}
            if not nuevo in animes:
                    animes.append(nuevo)
            self.__mongo.db.Productores.update_one({'_id':productor['_id']},{'$set':{'animes':animes}})
            productor = {'_id':productor['_id'], 'nombre':productor['nombre']}

        return productor

    
    #Funcion para establecer o crear referencias a la colección Manga
    def check_manga(self, titulo, animeId, tituloAnime):

        manga = self.existe_manga(titulo)

        if manga is None:
            if type(titulo) is dict:
                titulo = titulo['nombre']
            nuevo_manga = {
                'titulo': titulo,
                'numero_capitulos': 1,
                'genero':[],
                'escritor':None
            }

            manga = self.__mongo.db.Mangas.insert_one(nuevo_manga)
            manga = {'_id':manga.inserted_id, 'titulo':titulo}
        else:
            manga = {'_id':manga['_id'], 'titulo':manga['titulo']}

        return manga


    #Para obtener todos los escritores
    def get_animes(self):
        animes = self.__mongo.db.Animes.find()
        animes = json_util.dumps(animes)
        return Response(animes, mimetype='application/json')


    #Para obtener un escritor por medio de su ID
    def get_anime(self, id):
        try:
            anime = self.__mongo.db.Animes.find_one({'_id': ObjectId(id)})
            anime = json_util.dumps(anime)
        except Exception as ex:
            return jsonify({"status":404,"message":"Not Found"})

        return Response(anime, mimetype='application/json')

    #Eliminar un escritor por medio de su ID
    def delete_anime(self, id):
        self.__mongo.db.Animes.delete_one({'_id': ObjectId(id)})
        resp = {'message':'delete '+ id + ' successfully', 'status':200}
        resp = json_util.dumps(resp)

        return Response(resp, mimetype='application/json')


    #Actualizar algun dato del escritor
    def update_anime(self, id, request):
        resp = {}

        titulo = request.json['titulo']
        numero_episodios = request.json['numero_episodios']
        lista_episodios = request.json['lista_episodios']
        genero = request.json['genero']
        personajes = request.json['personajes']
        productor = request.json['productor']
        manga = request.json['manga']

        if titulo and numero_episodios and type(lista_episodios) is list and type(genero) is list and type(personajes) is list and productor and manga:

            
            self.__mongo.db.Animes.update_one({'_id':ObjectId(id)},{'$set':{'titulo':titulo,'numero_episodios':numero_episodios}})
            
            listaEpisodios = []
            if len(lista_episodios) >= 1:
                listaEpisodios = self.check_episodios(lista_episodios, id, tituloAnime=titulo)
                self.__mongo.db.Animes.update_one({'_id': ObjectId(id)},{'$set': {
                'lista_episodios':listaEpisodios
                }} )

            listaGeneros = []
            if len(genero) >= 1:
                listaGeneros = self.check_generos(genero, animeId=id, tituloAnime=titulo)
                self.__mongo.db.Animes.update_one({'_id': ObjectId(id)},{'$set': {
                'genero':listaGeneros
                }} )
            listaPersonajes = []
            if len(personajes) >= 1:
                listaPersonajes = self.check_personajes(personajes, animeId=id, tituloAnime=titulo)
                self.__mongo.db.Animes.update_one({'_id': ObjectId(id)},{'$set': {
                'personajes':listaPersonajes
                }} )
            productorId = self.check_productor(productor, animeId=id, tituloAnime=titulo)
            self.__mongo.db.Animes.update_one({'_id': ObjectId(id)},{'$set': {'productor':productorId}} )

            mangaId = self.check_manga(manga, id, titulo)
            self.__mongo.db.Animes.update_one({'_id': ObjectId(id)},{'$set': {'manga':mangaId}} )

            
            resp = {'message':'update '+ id + ' successfully', 'status':200}
        else:
            resp = {'message':'datos incompletos','status':406}

        
        resp = json_util.dumps(resp)
        return Response(resp, mimetype='application/json')
