from flask_migrate import Migrate
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from .excpetion import register_handle_exception
from .middleware.middleware import MiddlewareManager
from .vgenerator import VGenerator
from .seeds import *

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
code_generator = VGenerator()
middleware_manager = MiddlewareManager()
authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
}
api = Api(prefix='/api', security='Bearer Auth', authorizations=authorizations)
register_handle_exception(api)
