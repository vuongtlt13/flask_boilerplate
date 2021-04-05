from api.core import auth
from api.core.route import BaseRoute
from api.company.controller import CompanyController
from api.company.schema import CreateCompanyRequest, UpdateCompanyRequest, CompanyPaginateResponse, CompanyResponse
from extensions import api

ns = api.namespace('companies', description='Company operations')

__all__ = [
    "CreateCompanyRoute",
    "CompanyCommonRoute"
]


@ns.route('')
class CreateCompanyRoute(BaseRoute):
    def get_controller(self):
        return CompanyController

    @ns.doc("list_companies")
    @ns.marshal_with(CompanyPaginateResponse)
    @auth.login_required
    def get(self):
        return self.controller.get()

    @ns.doc("create_new_company")
    @ns.marshal_with(CompanyResponse)
    @ns.expect(CreateCompanyRequest)
    @auth.login_required
    def post(self):
        data = api.payload
        return self.controller.create(data=data)


@ns.route('/<int:_id>')
@ns.param('_id', 'ID of Company')
class CompanyCommonRoute(BaseRoute):
    def get_controller(self):
        return CompanyController

    @ns.doc('get_company_by_id')
    @ns.marshal_with(CompanyResponse)
    @auth.login_required
    def get(self, _id):
        return self.controller.get(_id)

    @ns.doc("update_company_by_id")
    @ns.marshal_with(CompanyResponse)
    @ns.expect(UpdateCompanyRequest)
    @auth.login_required
    def put(self, _id):
        data = api.payload
        return self.controller.update(_id=_id, data=data)

    @ns.doc("delete_company_by_id")
    @auth.login_required
    def delete(self, _id):
        return self.controller.delete(_id=_id)
