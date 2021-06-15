from flask import Request
from flask_jwt_extended import current_user

from api.user.user_type import UserType
from extensions.middleware.middleware import BaseMiddleware


class AdminVerify(BaseMiddleware):
    def handle(self, request: Request):
        from api.user.model import User
        user: User = current_user
        if user.user_type != UserType.ADMIN:
            from extensions.excpetion import PermissionDenied
            raise PermissionDenied("Forbidden")
