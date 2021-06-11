from flask_jwt_extended import jwt_required
from api.core.route import BaseRoute
from api.user_profile.controller import UserProfileController
from api.user_profile.schema import CreateUserProfileRequest, UpdateUserProfileRequest, UserProfilePaginateResponse, UserProfileResponse
from extensions import api

ns = api.namespace('user_profiles', description='UserProfile operations')

__all__ = [
    "CreateUserProfileRoute",
    "UserProfileCommonRoute"
]


@ns.route('')
class CreateUserProfileRoute(BaseRoute):
    def get_controller(self):
        return UserProfileController

    @ns.doc("list_user_profiles")
    @ns.marshal_with(UserProfilePaginateResponse)
    @jwt_required()
    def get(self):
        return self.controller.get()

    @ns.doc("create_new_user_profile")
    @ns.marshal_with(UserProfileResponse)
    @ns.expect(CreateUserProfileRequest)
    @jwt_required()
    def post(self):
        data = api.payload
        return self.controller.create(data=data)


@ns.route('/<int:_id>')
@ns.param('_id', 'ID of UserProfile')
class UserProfileCommonRoute(BaseRoute):
    def get_controller(self):
        return UserProfileController

    @ns.doc('get_user_profile_by_id')
    @ns.marshal_with(UserProfileResponse)
    @jwt_required()
    def get(self, _id):
        return self.controller.get(_id)

    @ns.doc("update_user_profile_by_id")
    @ns.marshal_with(UserProfileResponse)
    @ns.expect(UpdateUserProfileRequest)
    @jwt_required()
    def put(self, _id):
        data = api.payload
        return self.controller.update(_id=_id, data=data)

    @ns.doc("delete_user_profile_by_id")
    @jwt_required()
    def delete(self, _id):
        return self.controller.delete(_id=_id)
