import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    # SQLALCHEMY Config
    SQLALCHEMY_ECHO = (True, False)[os.getenv("SQLALCHEMY_ECHO", "false").lower() == "false"]
    SQLALCHEMY_DIALECT = os.getenv("SQLALCHEMY_DIALECT", "mysql")
    SQLALCHEMY_DRIVER = os.getenv("SQLALCHEMY_DRIVER", "pymysql")
    SQLALCHEMY_HOSTNAME = os.getenv("SQLALCHEMY_HOSTNAME", "localhost")
    SQLALCHEMY_PORT = os.getenv("SQLALCHEMY_PORT", 3306)
    SQLALCHEMY_DBNAME = os.getenv("SQLALCHEMY_DBNAME", "flask_test")
    SQLALCHEMY_USERNAME = os.getenv("SQLALCHEMY_USERNAME", "flask_test")
    SQLALCHEMY_PASSWORD = os.getenv("SQLALCHEMY_PASSWORD", "123456")
    SQLALCHEMY_DATABASE_URI = f'{SQLALCHEMY_DIALECT}' \
                              f'{(f"+{SQLALCHEMY_DRIVER}", "")[SQLALCHEMY_DRIVER is None or SQLALCHEMY_DRIVER == ""]}' \
                              f'://{SQLALCHEMY_USERNAME}:{SQLALCHEMY_PASSWORD}@{SQLALCHEMY_HOSTNAME}:{SQLALCHEMY_PORT}/{SQLALCHEMY_DBNAME}'

    # Flask Config
    FLASK_ENV = os.getenv("FLASK_ENV", 'production')
    DEBUG = False
    TESTING = False
    DATABASE_URI = SQLALCHEMY_DATABASE_URI
    SERVER_NAME = f'{os.getenv("APP_HOST", "localhost")}:{os.getenv("APP_PORT", 5000)}'
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")


class ProductionConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True

    # Design SQLALCHEMY Config
    DESIGN_SQLALCHEMY_DIALECT = os.getenv("DESIGN_SQLALCHEMY_DIALECT", "mysql")
    DESIGN_SQLALCHEMY_DRIVER = os.getenv("DESIGN_SQLALCHEMY_DRIVER", "pymysql")
    DESIGN_SQLALCHEMY_HOSTNAME = os.getenv("DESIGN_SQLALCHEMY_HOSTNAME", "localhost")
    DESIGN_SQLALCHEMY_PORT = os.getenv("DESIGN_SQLALCHEMY_PORT", 3306)
    DESIGN_SQLALCHEMY_DBNAME = os.getenv("DESIGN_SQLALCHEMY_DBNAME", "design_table")
    DESIGN_SQLALCHEMY_USERNAME = os.getenv("DESIGN_SQLALCHEMY_USERNAME", "root")
    DESIGN_SQLALCHEMY_PASSWORD = os.getenv("DESIGN_SQLALCHEMY_PASSWORD", "root")
    DESIGN_SQLALCHEMY_DATABASE_URI = f'{DESIGN_SQLALCHEMY_DIALECT}' \
                                     f'{(f"+{DESIGN_SQLALCHEMY_DRIVER}", "")[DESIGN_SQLALCHEMY_DRIVER is None or DESIGN_SQLALCHEMY_DRIVER == ""]}' \
                                     f'://{DESIGN_SQLALCHEMY_USERNAME}:{DESIGN_SQLALCHEMY_PASSWORD}@{DESIGN_SQLALCHEMY_HOSTNAME}:{DESIGN_SQLALCHEMY_PORT}/{DESIGN_SQLALCHEMY_DBNAME}'


class TestingConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True


config_map = {
    "production": ProductionConfig,
    "develop": DevelopmentConfig,
    "test": TestingConfig
}


def get_config(mode: str = None):
    mode = (mode or os.getenv("APP_MODE", "develop")).lower()
    return config_map.get(mode, DevelopmentConfig)
