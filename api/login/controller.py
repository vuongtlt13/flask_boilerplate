from typing import Dict
from flask import request
from werkzeug.security import check_password_hash

from api.core import auth
from api.user.repository import UserRepository
from extensions import response


class LoginController:
    def __init__(self):
        super().__init__()
        self.repository = UserRepository()

    def login(self, data: Dict):
        username = data.get('username', None)
        password = data.get('password', None)
        if password and username:
            user = self.repository.find_by_column(column='username', value=username)
            if user:
                if check_password_hash(user.password, password):
                    access_token = auth.encode_auth_token(user)
                    return response.success({
                        "access_token": access_token
                    })
        return response.error(error="username or password is invalid", code=401)
