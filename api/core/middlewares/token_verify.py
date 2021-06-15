from flask import Request
from flask_jwt_extended import current_user, verify_jwt_in_request

from extensions.excpetion import UserBlockedException
from extensions.middleware.middleware import BaseMiddleware


class TokenVerify(BaseMiddleware):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def handle(self, request: Request):
        verify_jwt_in_request(*self.args, **self.kwargs)
        from api.user.model import User
        user: User = current_user
        if not user.is_active:
            raise UserBlockedException("User blocked!")
        return 0
