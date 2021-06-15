from api.core.middlewares.token_verify import TokenVerify
from api.core.route import BaseRoute
from api.license_template_option.controller import LicenseTemplateOptionController
from api.license_template_option.schema import CreateLicenseTemplateOptionRequest, UpdateLicenseTemplateOptionRequest, LicenseTemplateOptionPaginateResponse, LicenseTemplateOptionResponse
from extensions import api, middleware_manager

ns = api.namespace('license_template_options', description='LicenseTemplateOption operations')

__all__ = [
    "CreateLicenseTemplateOptionRoute",
    "LicenseTemplateOptionCommonRoute"
]


@ns.route('')
@middleware_manager.route_middleware(TokenVerify)
class CreateLicenseTemplateOptionRoute(BaseRoute):
    def get_controller(self):
        return LicenseTemplateOptionController

    @ns.doc("list_license_template_options")
    @ns.marshal_with(LicenseTemplateOptionPaginateResponse)
    def get(self):
        return self.controller.get()

    @ns.doc("create_new_license_template_option")
    @ns.marshal_with(LicenseTemplateOptionResponse)
    @ns.expect(CreateLicenseTemplateOptionRequest)
    def post(self):
        data = api.payload
        return self.controller.create(data=data)


@ns.route('/<int:_id>')
@ns.param('_id', 'ID of LicenseTemplateOption')
@middleware_manager.route_middleware(TokenVerify)
class LicenseTemplateOptionCommonRoute(BaseRoute):
    def get_controller(self):
        return LicenseTemplateOptionController

    @ns.doc('get_license_template_option_by_id')
    @ns.marshal_with(LicenseTemplateOptionResponse)
    def get(self, _id):
        return self.controller.get(_id)

    @ns.doc("update_license_template_option_by_id")
    @ns.marshal_with(LicenseTemplateOptionResponse)
    @ns.expect(UpdateLicenseTemplateOptionRequest)
    def put(self, _id):
        data = api.payload
        return self.controller.update(_id=_id, data=data)

    @ns.doc("delete_license_template_option_by_id")
    def delete(self, _id):
        return self.controller.delete(_id=_id)
