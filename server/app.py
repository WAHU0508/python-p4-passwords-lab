#!/usr/bin/env python3

from flask import request, session, make_response, jsonify
from flask_restful import Resource

from config import app, db, api
from models import User

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

class Signup(Resource):
    
    def post(self):
        json = request.get_json()
        user = User(
            username=json['username']
        )
        user.password_hash = json['password']
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201

class CheckSession(Resource):
    
    def get(self):
        user = User.query.filter(User.id == session.get('user_id')).first()
        if user:
            user_dict = user.to_dict()
            return make_response(jsonify(user_dict), 200)
        else:
            response_body = {}
            return make_response(jsonify(response_body), 204)

class Login(Resource):

    def post(self):

        data = request.json
        username = data.get('username')
        password = data.get('password')
        user = User.query.filter(User.username == username).first()

        if user and user.authenticate(password):
            session['user_id'] = user.id
            return make_response(jsonify(user.to_dict()), 200)

        return make_response(jsonify({'error': 'Invalid username or password'}), 401)

class Logout(Resource):
    
    def delete(self):
        session['user_id'] = None
        return make_response(jsonify({}), 204)

api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(CheckSession, '/ckeck_session', endpoint='check_session')
if __name__ == '__main__':
    app.run(port=5555, debug=True)
