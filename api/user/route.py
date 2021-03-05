from api.core.route import BaseRoute
from api.user.controller import UserController
from api.user.schema import CreateUserRequest, UpdateUserRequest, UserPaginateResponse, UserResponse
from extensions import api

ns = api.namespace('users', description='User operations')


@ns.route('')
class CreateUserRoute(BaseRoute):
    def get_controller(self):
        return UserController

    @ns.doc("list_users")
    @ns.marshal_with(UserPaginateResponse)
    def get(self):
        return self.controller.get()

    @ns.doc("create_new_user")
    @ns.marshal_with(UserResponse)
    @ns.expect(CreateUserRequest)
    def post(self):
        data = api.payload
        return self.controller.create(data=data)


@ns.route('/<int:id>')
@ns.param('id', 'ID of User')
class UserCommonRoute(BaseRoute):
    def get_controller(self):
        return UserController

    @ns.doc('get_user_by_id')
    @ns.marshal_with(UserResponse)
    def get(self, id):
        return self.controller.get(id)

    @ns.doc("update_user_by_id")
    @ns.marshal_with(UserResponse)
    @ns.expect(UpdateUserRequest)
    def put(self, id):
        data = api.payload
        return self.controller.update(id=id, data=data)

    @ns.doc("delete_user_by_id")
    def delete(self, id):
        return self.controller.delete(id=id)
