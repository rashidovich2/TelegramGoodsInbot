from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the database URI and track modifications value from environment variables
db_uri = os.getenv('SQLALCHEMY_DATABASE_FULL_URI')
track_modifications = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = track_modifications
app.debug = True
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)
