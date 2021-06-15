from api.core.middlewares.token_verify import TokenVerify
from api.core.route import BaseRoute
from api.license_option.controller import LicenseOptionController
from api.license_option.schema import CreateLicenseOptionRequest, UpdateLicenseOptionRequest, LicenseOptionPaginateResponse, LicenseOptionResponse
from extensions import api, middleware_manager

ns = api.namespace('license_options', description='LicenseOption operations')

__all__ = [
    "CreateLicenseOptionRoute",
    "LicenseOptionCommonRoute"
]


@ns.route('')
@middleware_manager.route_middleware(TokenVerify)
class CreateLicenseOptionRoute(BaseRoute):
    def get_controller(self):
        return LicenseOptionController

    @ns.doc("list_license_options")
    @ns.marshal_with(LicenseOptionPaginateResponse)
    def get(self):
        return self.controller.get()

    @ns.doc("create_new_license_option")
    @ns.marshal_with(LicenseOptionResponse)
    @ns.expect(CreateLicenseOptionRequest)
    def post(self):
        data = api.payload
        return self.controller.create(data=data)


@ns.route('/<int:_id>')
@ns.param('_id', 'ID of LicenseOption')
@middleware_manager.route_middleware(TokenVerify)
class LicenseOptionCommonRoute(BaseRoute):
    def get_controller(self):
        return LicenseOptionController

    @ns.doc('get_license_option_by_id')
    @ns.marshal_with(LicenseOptionResponse)
    def get(self, _id):
        return self.controller.get(_id)

    @ns.doc("update_license_option_by_id")
    @ns.marshal_with(LicenseOptionResponse)
    @ns.expect(UpdateLicenseOptionRequest)
    def put(self, _id):
        data = api.payload
        return self.controller.update(_id=_id, data=data)

    @ns.doc("delete_license_option_by_id")
    def delete(self, _id):
        return self.controller.delete(_id=_id)
