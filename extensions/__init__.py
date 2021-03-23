from flask_migrate import Migrate
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from .vgenerator import *

db = SQLAlchemy()
migrate = Migrate()
api = Api(prefix='/api')
