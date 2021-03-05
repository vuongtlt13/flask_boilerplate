from api.core.route import BaseRoute
from api.user.controller import UserController
from extensions import api


@api.resource('/users')
class CreateUserRoute(BaseRoute):
    def get_controller(self):
        return UserController

    def get(self):
        return self.controller.get()

    def post(self):
        return self.controller.create()


@api.resource('/users/<int:id>')
class UserCommonRoute(BaseRoute):
    def get_controller(self):
        return UserController

    def get(self, id):
        return self.controller.get(id)

    def put(self, id):
        return self.controller.update(id=id)

    def delete(self, id):
        return self.controller.delete(id=id)
