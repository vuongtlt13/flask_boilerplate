from flask_jwt_extended import jwt_required
from api.core.route import BaseRoute
from api.application_config.controller import ApplicationConfigController
from api.application_config.schema import CreateApplicationConfigRequest, UpdateApplicationConfigRequest, ApplicationConfigPaginateResponse, ApplicationConfigResponse
from extensions import api

ns = api.namespace('application_configs', description='ApplicationConfig operations')

__all__ = [
    "CreateApplicationConfigRoute",
    "ApplicationConfigCommonRoute"
]


@ns.route('')
class CreateApplicationConfigRoute(BaseRoute):
    def get_controller(self):
        return ApplicationConfigController

    @ns.doc("list_application_configs")
    @ns.marshal_with(ApplicationConfigPaginateResponse)
    @jwt_required()
    def get(self):
        return self.controller.get()

    @ns.doc("create_new_application_config")
    @ns.marshal_with(ApplicationConfigResponse)
    @ns.expect(CreateApplicationConfigRequest)
    @jwt_required()
    def post(self):
        data = api.payload
        return self.controller.create(data=data)


@ns.route('/<int:_id>')
@ns.param('_id', 'ID of ApplicationConfig')
class ApplicationConfigCommonRoute(BaseRoute):
    def get_controller(self):
        return ApplicationConfigController

    @ns.doc('get_application_config_by_id')
    @ns.marshal_with(ApplicationConfigResponse)
    @jwt_required()
    def get(self, _id):
        return self.controller.get(_id)

    @ns.doc("update_application_config_by_id")
    @ns.marshal_with(ApplicationConfigResponse)
    @ns.expect(UpdateApplicationConfigRequest)
    @jwt_required()
    def put(self, _id):
        data = api.payload
        return self.controller.update(_id=_id, data=data)

    @ns.doc("delete_application_config_by_id")
    @jwt_required()
    def delete(self, _id):
        return self.controller.delete(_id=_id)
