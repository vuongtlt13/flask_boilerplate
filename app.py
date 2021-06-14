from flask import Flask

from config import get_config
from extensions import db, migrate, api, code_generator, secret_generator_cli, seeds, jwt, middleware_manager

try:
    import api as api_route
except Exception as e:
    raise
    print(e)
    pass


def create_app(conf=None) -> Flask:
    conf = conf or get_config()
    app = Flask(__name__)
    app.config.from_object(conf)

    # register with app
    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    middleware_manager.init_app(app)
    jwt.init_app(app)
    secret_generator_cli.init_app(app)
    if conf.DEBUG:
        code_generator.init_app(app)
        seeds.init_app(app)

    return app


if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run()
