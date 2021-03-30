from api.core.route import BaseRoute
from api.service.controller import ServiceController
from api.service.schema import CreateServiceRequest, UpdateServiceRequest, ServicePaginateResponse, ServiceResponse
from extensions import api

ns = api.namespace('services', description='Service operations')

__all__ = [
    "CreateServiceRoute",
    "ServiceCommonRoute"
]


@ns.route('')
class CreateServiceRoute(BaseRoute):
    def get_controller(self):
        return ServiceController

    @ns.doc("list_services")
    @ns.marshal_with(ServicePaginateResponse)
    def get(self):
        return self.controller.get()

    @ns.doc("create_new_service")
    @ns.marshal_with(ServiceResponse)
    @ns.expect(CreateServiceRequest)
    def post(self):
        data = api.payload
        return self.controller.create(data=data)


@ns.route('/<int:id>')
@ns.param('id', 'ID of Service')
class ServiceCommonRoute(BaseRoute):
    def get_controller(self):
        return ServiceController

    @ns.doc('get_service_by_id')
    @ns.marshal_with(ServiceResponse)
    def get(self, _id):
        return self.controller.get(_id)

    @ns.doc("update_service_by_id")
    @ns.marshal_with(ServiceResponse)
    @ns.expect(UpdateServiceRequest)
    def put(self, _id):
        data = api.payload
        return self.controller.update(_id=_id, data=data)

    @ns.doc("delete_service_by_id")
    def delete(self, _id):
        return self.controller.delete(_id=_id)
