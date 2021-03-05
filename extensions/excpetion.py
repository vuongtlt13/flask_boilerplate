import traceback

from flask import Flask
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import InternalServerError

from extensions import response

DATABASE_DUPLICATE_ERROR_CODE = 1062


def init_app(app: Flask):
    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, IntegrityError):
            code = e.orig.args[0]
            if code == DATABASE_DUPLICATE_ERROR_CODE:
                detail = e.orig.args[1]
                return response.error(error=detail, code=400)

        if app.config['DEBUG']:
            error = str(e)
        else:
            error = "Unknown error!"
        traceback.print_exc()
        return response.error(error=error, code=400)

    @app.errorhandler(InternalServerError)
    def handle_500(e):
        if app.config['DEBUG']:
            error = str(e)
        else:
            error = "Unknown error!"
        traceback.print_exc()
        return response.error(code=500, error=error)
