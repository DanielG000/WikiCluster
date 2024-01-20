from flask import request, Response, jsonify
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId

class ModelUsers:

    def __init__(self, app):
        self.__mongo = PyMongo(app)

    def create_user(self, request):
        resp = {}

        username = request.json['username']
        email = request.json['email']
        password = request.json['password']

        if username and email and password:
            hashed_pass = generate_password_hash(password)
            newuser = {'username':username,'email':email,'password':hashed_pass}
            newUserId = self.__mongo.db.users.insert_one(newuser)
            resp = jsonify({'_id': str(newUserId.inserted_id),
                        'username': username,
                        'email': email,
                        'password': hashed_pass})
        else:
            resp = jsonify({'message':'datos incompletos','status':406})

        return resp

    def get_users(self):
        users = self.__mongo.db.users.find()
        users = json_util.dumps(users)
        return Response(users, mimetype='application/json')

    
    def get_user(self, id):
        try:
            user = self.__mongo.db.users.find_one({'_id': ObjectId(id)})
            user = json_util.dumps(user)
        except Exception as ex:
            return jsonify({"status":404,"message":"Not Found"})

        return Response(user, mimetype='application/json')


    def delete_user(self, id):
        self.__mongo.db.users.delete_one({'_id': ObjectId(id)})
        resp = jsonify({'message':'delete '+ id + ' successfully', 'status':200})

        return resp



    def update_user(self, id, request):

        username = request.json['username']
        email = request.json['email']
        password = request.json['password']
        resp = {}

        if username and email and password:
            hashed_pass = generate_password_hash(password)
            self.__mongo.db.users.update_one({'_id': ObjectId(id)},{'$set': {
                'username':username,
                'password':hashed_pass,
                'email': email
                }} )
            resp = jsonify({'message':'update '+ id + ' successfully', 'status':200})
        else:
            resp = jsonify({'message':'datos incompletos','status':406})


        return resp
