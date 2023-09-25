from sqlalchemy import MetaData, Column, BigInteger, Text, Integer, DateTime
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

#class UserSchema(ma.Schema):
#        fields = ('user_id', 'increment', 'user_login', 'user_name', 'user_lang', 'user_balance', 'user_hold', 'user_refill', 'user_date', 'user_unix', 'user_city', 'user_ads', 'user_phone', 'user_geocode', 'user_role', 'user_city_id', 'promocode', 'free_delivery_point', 'delivery_rate', 'new_prod_notify')

class UserSchema(ma.Schema):
    increment = fields.Integer()
    user_id = fields.Integer()
    user_login = fields.Str()
    user_name = fields.Str()
    user_lang = fields.Str()
    user_balance = fields.Integer()
    user_hold = fields.Integer()
    user_refill = fields.Integer()
    user_date = fields.DateTime()
    user_unix = fields.Integer()
    user_city = fields.Str()
    user_address = fields.Str()
    user_phone = fields.Str()
    user_geocode = fields.Str()
    user_role = fields.Str()
    user_city_id = fields.Integer()
    promocode = fields.Str()
    free_delivery_point = fields.Integer()
    delivery_rate = fields.Integer()
    new_prod_notify = fields.Integer()

user_schema = UserSchema()
users_schema = UserSchema(many=True)
