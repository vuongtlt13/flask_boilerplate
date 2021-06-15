from api.core.middlewares.token_verify import TokenVerify
from api.core.route import BaseRoute
from api.license.controller import LicenseController
from api.license.schema import CreateLicenseRequest, UpdateLicenseRequest, LicensePaginateResponse, LicenseResponse
from extensions import api, middleware_manager

ns = api.namespace('licenses', description='License operations')

__all__ = [
    "CreateLicenseRoute",
    "LicenseCommonRoute"
]


@ns.route('')
@middleware_manager.route_middleware(TokenVerify)
class CreateLicenseRoute(BaseRoute):
    def get_controller(self):
        return LicenseController

    @ns.doc("list_licenses")
    @ns.marshal_with(LicensePaginateResponse)
    def get(self):
        return self.controller.get()

    @ns.doc("create_new_license")
    @ns.marshal_with(LicenseResponse)
    @ns.expect(CreateLicenseRequest)
    def post(self):
        data = api.payload
        return self.controller.create(data=data)


@ns.route('/<int:_id>')
@ns.param('_id', 'ID of License')
@middleware_manager.route_middleware(TokenVerify)
class LicenseCommonRoute(BaseRoute):
    def get_controller(self):
        return LicenseController

    @ns.doc('get_license_by_id')
    @ns.marshal_with(LicenseResponse)
    def get(self, _id):
        return self.controller.get(_id)

    @ns.doc("update_license_by_id")
    @ns.marshal_with(LicenseResponse)
    @ns.expect(UpdateLicenseRequest)
    def put(self, _id):
        data = api.payload
        return self.controller.update(_id=_id, data=data)

    @ns.doc("delete_license_by_id")
    def delete(self, _id):
        return self.controller.delete(_id=_id)
