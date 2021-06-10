from flask_jwt_extended import jwt_required
from api.core.route import BaseRoute
from api.user.controller import UserController
from api.user.schema import CreateUserRequest, UpdateUserRequest, UserPaginateResponse, UserResponse
from extensions import api

ns = api.namespace('users', description='User operations')

__all__ = [
    "CreateUserRoute",
    "UserCommonRoute"
]


@ns.route('')
class CreateUserRoute(BaseRoute):
    def get_controller(self):
        return UserController

    @ns.doc("list_users")
    @ns.marshal_with(UserPaginateResponse)
    @jwt_required()
    def get(self):
        return self.controller.get()

    @ns.doc("create_new_user")
    @ns.marshal_with(UserResponse)
    @ns.expect(CreateUserRequest)
    @jwt_required()
    def post(self):
        data = api.payload
        return self.controller.create(data=data)


@ns.route('/<int:_id>')
@ns.param('_id', 'ID of User')
class UserCommonRoute(BaseRoute):
    def get_controller(self):
        return UserController

    @ns.doc('get_user_by_id')
    @ns.marshal_with(UserResponse)
    @jwt_required()
    def get(self, _id):
        return self.controller.get(_id)

    @ns.doc("update_user_by_id")
    @ns.marshal_with(UserResponse)
    @ns.expect(UpdateUserRequest)
    @jwt_required()
    def put(self, _id):
        data = api.payload
        return self.controller.update(_id=_id, data=data)

    @ns.doc("delete_user_by_id")
    @jwt_required()
    def delete(self, _id):
        return self.controller.delete(_id=_id)
