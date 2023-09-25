from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from models import User
from schemas import UserSchema
from app import app


class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        return users_schema.dump(users)

    '''def post(self):
        new_user = User(
            increment=request.json['increment'],
            user_login=request.json['user_login'],
            user_name=request.json['user_name'],
            user_lang=request.json['user_lang'],
            user_balance=request.json['user_balance'],
            user_hold=request.json['user_hold'],
            user_refill=request.json['user_refill'],
            user_date=request.json['user_date'],
            user_unix=request.json['user_unix'],
            user_city=request.json['user_city'],
            user_ads=request.json['user_ads'],
            user_phone=request.json['user_phone'],
            user_geocode=request.json['user_geocode'],
            user_role=request.json['user_role'],
            user_city_id=request.json['user_city_id'],
            promocode=request.json['promocode'],
            free_delivery_point=request.json['free_delivery_point'],
            delivery_rate=request.json['delivery_rate'],
            new_prod_notify=request.json['new_prod_notify']
        )
        db.session.add(new_user)
        db.session.commit()
        return user_schema.dump(new_user)'''

class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return user_schema.dump(user)

        '''def patch(self, user_id):
        user = User.query.get_or_404(user_id)

        if 'increment' in request.json:
            user.increment = request.json['increment']
        if 'user_login' in request.json:
            user.user_login = request.json['user_login']
        # Update other fields here...'''

        db.session.commit()
        return user_schema.dump(user)

    '''def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204'''

api.add_resource('/', endpoint='index')
api.add_resource('/about', endpoint='about')
api.add_resource(UserListResource, '/users', endpoint='users')
api.add_resource(UserResource, '/users/<int:user_id>', endpoint='user')

