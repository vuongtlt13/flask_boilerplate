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
    DEBUG = False
    TESTING = False
    DATABASE_URI = f'{SQLALCHEMY_DIALECT}' \
                   f'{(f"+{SQLALCHEMY_DRIVER}", "")[SQLALCHEMY_DRIVER is None or SQLALCHEMY_DRIVER == ""]}' \
                   f'://{SQLALCHEMY_USERNAME}:{SQLALCHEMY_PASSWORD}@{SQLALCHEMY_HOSTNAME}:{SQLALCHEMY_PORT}/{SQLALCHEMY_DBNAME}'
    SERVER_NAME = f'{os.getenv("APP_HOST", "localhost")}:{os.getenv("APP_PORT", 5000)}'


class ProductionConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True


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
