from sqlalchemy import MetaData, Column, BigInteger, Text, Integer, TimeStamp
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
from app import app

db = SQLAlchemy(metadata=MetaData()) #metadata=MetaData()

class User(db.Model):
    __tablename__ = 'users'

    increment = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.Integer)
    user_login = db.Column(db.String(50))
    user_name = db.Column(db.String(50))
    user_lang = db.Column(db.String(50))
    user_balance = db.Column(db.BigInteger)
    user_hold = db.Column(db.BigInteger)
    user_refill = db.Column(db.Integer)
    user_date = db.Column(db.DateTime)
    user_unix = db.Column(db.Integer)
    user_city = db.Column(db.String(50))
    user_address = db.Column(db.String(50))
    user_phone = db.Column(db.String(50))
    user_geocode = db.Column(db.String(50))
    user_role = db.Column(db.String(50))
    user_city_id = db.Column(db.BigInteger)
    promocode = db.Column(db.String(50))
    free_delivery_point = db.Column(db.BigInteger)
    delivery_rate = db.Column(db.BigInteger)
    new_prod_notify = db.Column(db.BigInteger)

    def __repr__(self):
        return f'<User {self.user_name}>'

class UserSchema(ma.Schema):
    class Meta:
        fields = ('increment', 'user_id', 'user_login', 'user_name', 'user_lang', 'user_balance', 'user_hold', 'user_refill', 'user_date', 'user_unix', 'user_city', 'user_address', 'user_phone', 'user_geocode', 'user_role', 'user_city_id', 'promocode', 'free_delivery_point', 'delivery_rate', 'new_prod_notify')

user_schema = UserSchema()
users_schema = UserSchema(many=True)