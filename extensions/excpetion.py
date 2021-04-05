import traceback

from flask import Flask
from werkzeug.exceptions import InternalServerError

from extensions import response


class VBaseException(Exception):
    response_code = 400

    def __init__(self, message: str, error_code: int = None):
        self.message = message
        self.error_code = error_code or self.response_code


class DatabaseDuplicateException(VBaseException):
    pass


class AccessTokenInvalid(VBaseException):
    response_code = 401


class AccessTokenMissing(VBaseException):
    response_code = 401


class AccessTokenExpired(VBaseException):
    response_code = 403


def init_app(app: Flask):
    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, VBaseException):
            return response.error(code=e.response_code, error={
                "code": e.error_code,
                "message": e.message
            })

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
