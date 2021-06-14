from flask import Request
from flask_jwt_extended import verify_jwt_in_request
from extensions.middleware.middleware import BaseMiddleware


class TokenVerify(BaseMiddleware):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def handle(self, request: Request):
        return verify_jwt_in_request(*self.args, **self.kwargs)
