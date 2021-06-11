from flask_jwt_extended import jwt_required
from api.core.route import BaseRoute
from api.license_template.controller import LicenseTemplateController
from api.license_template.schema import CreateLicenseTemplateRequest, UpdateLicenseTemplateRequest, LicenseTemplatePaginateResponse, LicenseTemplateResponse
from extensions import api

ns = api.namespace('license_templates', description='LicenseTemplate operations')

__all__ = [
    "CreateLicenseTemplateRoute",
    "LicenseTemplateCommonRoute"
]


@ns.route('')
class CreateLicenseTemplateRoute(BaseRoute):
    def get_controller(self):
        return LicenseTemplateController

    @ns.doc("list_license_templates")
    @ns.marshal_with(LicenseTemplatePaginateResponse)
    @jwt_required()
    def get(self):
        return self.controller.get()

    @ns.doc("create_new_license_template")
    @ns.marshal_with(LicenseTemplateResponse)
    @ns.expect(CreateLicenseTemplateRequest)
    @jwt_required()
    def post(self):
        data = api.payload
        return self.controller.create(data=data)


@ns.route('/<int:_id>')
@ns.param('_id', 'ID of LicenseTemplate')
class LicenseTemplateCommonRoute(BaseRoute):
    def get_controller(self):
        return LicenseTemplateController

    @ns.doc('get_license_template_by_id')
    @ns.marshal_with(LicenseTemplateResponse)
    @jwt_required()
    def get(self, _id):
        return self.controller.get(_id)

    @ns.doc("update_license_template_by_id")
    @ns.marshal_with(LicenseTemplateResponse)
    @ns.expect(UpdateLicenseTemplateRequest)
    @jwt_required()
    def put(self, _id):
        data = api.payload
        return self.controller.update(_id=_id, data=data)

    @ns.doc("delete_license_template_by_id")
    @jwt_required()
    def delete(self, _id):
        return self.controller.delete(_id=_id)
