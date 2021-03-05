from flask import Flask

from config import get_config
from extensions import db, list_route_cli, migrate, api, excpetion
from api import *


def create_app(conf=None) -> Flask:
    conf = conf or get_config()
    app = Flask(__name__)
    app.config.from_object(conf)

    # register with app
    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    list_route_cli.init_app(app)
    excpetion.init_app(app)

    # return
    return app


if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run()
