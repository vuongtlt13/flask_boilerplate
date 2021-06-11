from flask_jwt_extended import jwt_required
from api.core.route import BaseRoute
from api.license_option.controller import LicenseOptionController
from api.license_option.schema import CreateLicenseOptionRequest, UpdateLicenseOptionRequest, LicenseOptionPaginateResponse, LicenseOptionResponse
from extensions import api

ns = api.namespace('license_options', description='LicenseOption operations')

__all__ = [
    "CreateLicenseOptionRoute",
    "LicenseOptionCommonRoute"
]


@ns.route('')
class CreateLicenseOptionRoute(BaseRoute):
    def get_controller(self):
        return LicenseOptionController

    @ns.doc("list_license_options")
    @ns.marshal_with(LicenseOptionPaginateResponse)
    @jwt_required()
    def get(self):
        return self.controller.get()

    @ns.doc("create_new_license_option")
    @ns.marshal_with(LicenseOptionResponse)
    @ns.expect(CreateLicenseOptionRequest)
    @jwt_required()
    def post(self):
        data = api.payload
        return self.controller.create(data=data)


@ns.route('/<int:_id>')
@ns.param('_id', 'ID of LicenseOption')
class LicenseOptionCommonRoute(BaseRoute):
    def get_controller(self):
        return LicenseOptionController

    @ns.doc('get_license_option_by_id')
    @ns.marshal_with(LicenseOptionResponse)
    @jwt_required()
    def get(self, _id):
        return self.controller.get(_id)

    @ns.doc("update_license_option_by_id")
    @ns.marshal_with(LicenseOptionResponse)
    @ns.expect(UpdateLicenseOptionRequest)
    @jwt_required()
    def put(self, _id):
        data = api.payload
        return self.controller.update(_id=_id, data=data)

    @ns.doc("delete_license_option_by_id")
    @jwt_required()
    def delete(self, _id):
        return self.controller.delete(_id=_id)
