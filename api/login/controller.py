from typing import Dict
from flask import request
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from extensions import response

from api.user.repository import UserRepository


class LoginController:
    def __init__(self):
        super().__init__()
        self.repository = UserRepository()

    def login(self, data: Dict):
        email = data.get('email', None)
        password = data.get('password', None)
        if password and email:
            user = self.repository.find_by_column(column='email', value=email)
            if user:
                if check_password_hash(user.password, password):
                    access_token = create_access_token(identity=user)
                    return response.success({
                        "access_token": access_token
                    })
        return response.error(error="email or password is invalid", code=401)
