from flask_jwt_extended import jwt_required
from api.core.route import BaseRoute
from api.develop_device.controller import DevelopDeviceController
from api.develop_device.schema import CreateDevelopDeviceRequest, UpdateDevelopDeviceRequest, DevelopDevicePaginateResponse, DevelopDeviceResponse
from extensions import api

ns = api.namespace('develop_devices', description='DevelopDevice operations')

__all__ = [
    "CreateDevelopDeviceRoute",
    "DevelopDeviceCommonRoute"
]


@ns.route('')
class CreateDevelopDeviceRoute(BaseRoute):
    def get_controller(self):
        return DevelopDeviceController

    @ns.doc("list_develop_devices")
    @ns.marshal_with(DevelopDevicePaginateResponse)
    @jwt_required()
    def get(self):
        return self.controller.get()

    @ns.doc("create_new_develop_device")
    @ns.marshal_with(DevelopDeviceResponse)
    @ns.expect(CreateDevelopDeviceRequest)
    @jwt_required()
    def post(self):
        data = api.payload
        return self.controller.create(data=data)


@ns.route('/<int:_id>')
@ns.param('_id', 'ID of DevelopDevice')
class DevelopDeviceCommonRoute(BaseRoute):
    def get_controller(self):
        return DevelopDeviceController

    @ns.doc('get_develop_device_by_id')
    @ns.marshal_with(DevelopDeviceResponse)
    @jwt_required()
    def get(self, _id):
        return self.controller.get(_id)

    @ns.doc("update_develop_device_by_id")
    @ns.marshal_with(DevelopDeviceResponse)
    @ns.expect(UpdateDevelopDeviceRequest)
    @jwt_required()
    def put(self, _id):
        data = api.payload
        return self.controller.update(_id=_id, data=data)

    @ns.doc("delete_develop_device_by_id")
    @jwt_required()
    def delete(self, _id):
        return self.controller.delete(_id=_id)
