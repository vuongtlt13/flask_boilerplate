import os

from flask import Flask
from flask.cli import AppGroup
import dotenv
import secrets


def init_app(app: Flask):
    secret_cli = AppGroup('secret')

    @secret_cli.command('generate')
    def generate():
        dotenv_file = dotenv.find_dotenv()
        dotenv.load_dotenv(dotenv_file)

        os.environ["JWT_SECRET_KEY"] = secrets.token_urlsafe()
        print(os.environ['JWT_SECRET_KEY'])

        # os.environ["SECURITY_PASSWORD_SALT"] = str(secrets.SystemRandom().getrandbits(128))
        # print(os.environ['SECURITY_PASSWORD_SALT'])

        # Write changes to .env file.
        dotenv.set_key(dotenv_file, "JWT_SECRET_KEY", os.environ["JWT_SECRET_KEY"])
        # dotenv.set_key(dotenv_file, "SECURITY_PASSWORD_SALT", os.environ["SECURITY_PASSWORD_SALT"])

        print("Secrets generated successfully!")

    app.cli.add_command(secret_cli)
