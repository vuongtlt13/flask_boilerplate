from flask import Flask

from config import get_config
from extensions import db, migrate


def create_app(conf=None) -> Flask:
    conf = conf or get_config()
    app = Flask(__name__)
    app.config.from_object(conf)
    db.init_app(app)
    migrate.init_app(app, db)
    return app


if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run()
