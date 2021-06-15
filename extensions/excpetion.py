import traceback
from flask_jwt_extended.exceptions import NoAuthorizationError
from flask_restx import Api
from jwt import ExpiredSignatureError
from werkzeug.exceptions import InternalServerError


class VBaseException(Exception):
    response_code = 400

    def __init__(self, message: str):
        self.message = message


class DatabaseDuplicateException(VBaseException):
    pass


class UserBlockedException(VBaseException):
    response_code = 403


def register_handle_exception(api: Api):
    from extensions import response

    @api.errorhandler(ExpiredSignatureError)
    def handle_expired_token(e):
        return response.error(code=401, message="Session expired!")

    @api.errorhandler(NoAuthorizationError)
    def handle_missing_token(e):
        return response.error(code=401, message="Unauthorized")

    @api.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, VBaseException):
            return response.error(code=e.response_code, message=e.message)

        error = "Unknown error!"
        traceback.print_exc()
        return response.error(message=error, code=400)

    @api.errorhandler(InternalServerError)
    def handle_500(e):
        error = "Unknown error!"
        traceback.print_exc()
        return response.error(code=500, message=error)
