from api.core.middlewares.token_verify import TokenVerify
from api.core.route import BaseRoute
from api.application_config.controller import ApplicationConfigController
from api.application_config.schema import CreateApplicationConfigRequest, UpdateApplicationConfigRequest, ApplicationConfigPaginateResponse, ApplicationConfigResponse
from extensions import api, middleware_manager

ns = api.namespace('application_configs', description='ApplicationConfig operations')

__all__ = [
    "CreateApplicationConfigRoute",
    "ApplicationConfigCommonRoute"
]


@ns.route('')
@middleware_manager.route_middleware(TokenVerify)
class CreateApplicationConfigRoute(BaseRoute):
    def get_controller(self):
        return ApplicationConfigController

    @ns.doc("list_application_configs")
    @ns.marshal_with(ApplicationConfigPaginateResponse)
    def get(self):
        return self.controller.get()

    @ns.doc("create_new_application_config")
    @ns.marshal_with(ApplicationConfigResponse)
    @ns.expect(CreateApplicationConfigRequest)
    def post(self):
        data = api.payload
        return self.controller.create(data=data)


@ns.route('/<int:_id>')
@ns.param('_id', 'ID of ApplicationConfig')
@middleware_manager.route_middleware(TokenVerify)
class ApplicationConfigCommonRoute(BaseRoute):
    def get_controller(self):
        return ApplicationConfigController

    @ns.doc('get_application_config_by_id')
    @ns.marshal_with(ApplicationConfigResponse)
    def get(self, _id):
        return self.controller.get(_id)

    @ns.doc("update_application_config_by_id")
    @ns.marshal_with(ApplicationConfigResponse)
    @ns.expect(UpdateApplicationConfigRequest)
    def put(self, _id):
        data = api.payload
        return self.controller.update(_id=_id, data=data)

    @ns.doc("delete_application_config_by_id")
    def delete(self, _id):
        return self.controller.delete(_id=_id)
