import traceback
from flask_jwt_extended.exceptions import NoAuthorizationError
from flask_restx import Api
from werkzeug.exceptions import InternalServerError


class VBaseException(Exception):
    response_code = 400

    def __init__(self, message: str, error_code: int = None):
        self.message = message
        self.error_code = error_code or self.response_code


class DatabaseDuplicateException(VBaseException):
    pass


def register_handle_exception(api: Api):
    from extensions import response

    @api.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, VBaseException):
            return response.error(code=e.response_code, message=e.message)
        elif isinstance(e, NoAuthorizationError):
            return response.error(code=401, message=str(e))

        error = "Unknown error!"
        traceback.print_exc()
        return response.error(message=error, code=400)

    @api.errorhandler(InternalServerError)
    def handle_500(e):
        error = "Unknown error!"
        traceback.print_exc()
        return response.error(code=500, message=error)
