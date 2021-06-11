from flask_jwt_extended import jwt_required
from api.core.route import BaseRoute
from api.license.controller import LicenseController
from api.license.schema import CreateLicenseRequest, UpdateLicenseRequest, LicensePaginateResponse, LicenseResponse
from extensions import api

ns = api.namespace('licenses', description='License operations')

__all__ = [
    "CreateLicenseRoute",
    "LicenseCommonRoute"
]


@ns.route('')
class CreateLicenseRoute(BaseRoute):
    def get_controller(self):
        return LicenseController

    @ns.doc("list_licenses")
    @ns.marshal_with(LicensePaginateResponse)
    @jwt_required()
    def get(self):
        return self.controller.get()

    @ns.doc("create_new_license")
    @ns.marshal_with(LicenseResponse)
    @ns.expect(CreateLicenseRequest)
    @jwt_required()
    def post(self):
        data = api.payload
        return self.controller.create(data=data)


@ns.route('/<int:_id>')
@ns.param('_id', 'ID of License')
class LicenseCommonRoute(BaseRoute):
    def get_controller(self):
        return LicenseController

    @ns.doc('get_license_by_id')
    @ns.marshal_with(LicenseResponse)
    @jwt_required()
    def get(self, _id):
        return self.controller.get(_id)

    @ns.doc("update_license_by_id")
    @ns.marshal_with(LicenseResponse)
    @ns.expect(UpdateLicenseRequest)
    @jwt_required()
    def put(self, _id):
        data = api.payload
        return self.controller.update(_id=_id, data=data)

    @ns.doc("delete_license_by_id")
    @jwt_required()
    def delete(self, _id):
        return self.controller.delete(_id=_id)
