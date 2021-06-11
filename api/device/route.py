from flask_jwt_extended import jwt_required
from api.core.route import BaseRoute
from api.device.controller import DeviceController
from api.device.schema import CreateDeviceRequest, UpdateDeviceRequest, DevicePaginateResponse, DeviceResponse
from extensions import api

ns = api.namespace('devices', description='Device operations')

__all__ = [
    "CreateDeviceRoute",
    "DeviceCommonRoute"
]


@ns.route('')
class CreateDeviceRoute(BaseRoute):
    def get_controller(self):
        return DeviceController

    @ns.doc("list_devices")
    @ns.marshal_with(DevicePaginateResponse)
    @jwt_required()
    def get(self):
        return self.controller.get()

    @ns.doc("create_new_device")
    @ns.marshal_with(DeviceResponse)
    @ns.expect(CreateDeviceRequest)
    @jwt_required()
    def post(self):
        data = api.payload
        return self.controller.create(data=data)


@ns.route('/<int:_id>')
@ns.param('_id', 'ID of Device')
class DeviceCommonRoute(BaseRoute):
    def get_controller(self):
        return DeviceController

    @ns.doc('get_device_by_id')
    @ns.marshal_with(DeviceResponse)
    @jwt_required()
    def get(self, _id):
        return self.controller.get(_id)

    @ns.doc("update_device_by_id")
    @ns.marshal_with(DeviceResponse)
    @ns.expect(UpdateDeviceRequest)
    @jwt_required()
    def put(self, _id):
        data = api.payload
        return self.controller.update(_id=_id, data=data)

    @ns.doc("delete_device_by_id")
    @jwt_required()
    def delete(self, _id):
        return self.controller.delete(_id=_id)
