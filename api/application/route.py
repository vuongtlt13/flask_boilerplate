from flask_jwt_extended import jwt_required

from api.core.middlewares.token_verify import TokenVerify
from api.core.route import BaseRoute
from api.application.controller import ApplicationController
from api.application.schema import CreateApplicationRequest, UpdateApplicationRequest, ApplicationPaginateResponse, ApplicationResponse
from extensions import api, middleware_manager

ns = api.namespace('applications', description='Application operations')

__all__ = [
    "CreateApplicationRoute",
    "ApplicationCommonRoute"
]


@ns.route('')
@middleware_manager.route_middleware(TokenVerify)
class CreateApplicationRoute(BaseRoute):
    def get_controller(self):
        return ApplicationController

    @ns.doc("list_applications")
    @ns.marshal_with(ApplicationPaginateResponse)
    def get(self):
        return self.controller.get()

    @ns.doc("create_new_application")
    @ns.marshal_with(ApplicationResponse)
    @ns.expect(CreateApplicationRequest)
    def post(self):
        data = api.payload
        return self.controller.create(data=data)


@ns.route('/<int:_id>')
@ns.param('_id', 'ID of Application')
class ApplicationCommonRoute(BaseRoute):
    def get_controller(self):
        return ApplicationController

    @ns.doc('get_application_by_id')
    @ns.marshal_with(ApplicationResponse)
    @jwt_required()
    def get(self, _id):
        return self.controller.get(_id)

    @ns.doc("update_application_by_id")
    @ns.marshal_with(ApplicationResponse)
    @ns.expect(UpdateApplicationRequest)
    @jwt_required()
    def put(self, _id):
        data = api.payload
        return self.controller.update(_id=_id, data=data)

    @ns.doc("delete_application_by_id")
    @jwt_required()
    def delete(self, _id):
        return self.controller.delete(_id=_id)
