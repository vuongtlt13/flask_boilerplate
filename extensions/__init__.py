from flask_migrate import Migrate
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from .vgenerator import *
from .seeds import *

db = SQLAlchemy()
migrate = Migrate()

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
}
api = Api(prefix='/api', security='Bearer Auth', authorizations=authorizations)
