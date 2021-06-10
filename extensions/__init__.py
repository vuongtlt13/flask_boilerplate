from flask_migrate import Migrate
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from .vgenerator import VGenerator
from .seeds import *

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
code_generator = VGenerator()

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
}
api = Api(prefix='/api', security='Bearer Auth', authorizations=authorizations)
