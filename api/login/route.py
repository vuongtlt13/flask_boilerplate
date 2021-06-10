from api.core.route import BaseRoute
from api.login.controller import LoginController
from api.login.schema import LoginRequest, LoginResponse
from extensions import api

ns = api.namespace('auth', description='Authenticate operations')

__all__ = [
    "LoginCommonRoute",
]


@ns.route('/login')
class LoginCommonRoute(BaseRoute):
    def get_controller(self):
        return LoginController

    @ns.doc('login by email, password')
    @ns.marshal_with(LoginResponse)
    @ns.expect(LoginRequest)
    def post(self):
        data = api.payload
        return self.controller.login(data=data)
