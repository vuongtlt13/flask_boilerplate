from api.core import auth
from api.core.route import BaseRoute
from api.${singular_snake_case_model_name}.controller import ${singular_pascal_case_model_name}Controller
from api.${singular_snake_case_model_name}.schema import Create${singular_pascal_case_model_name}Request, Update${singular_pascal_case_model_name}Request, ${singular_pascal_case_model_name}PaginateResponse, ${singular_pascal_case_model_name}Response
from extensions import api

ns = api.namespace('${plural_snake_case_model_name}', description='${singular_pascal_case_model_name} operations')

__all__ = [
    "Create${singular_pascal_case_model_name}Route",
    "${singular_pascal_case_model_name}CommonRoute"
]


@ns.route('')
class Create${singular_pascal_case_model_name}Route(BaseRoute):
    def get_controller(self):
        return ${singular_pascal_case_model_name}Controller

    @ns.doc("list_${plural_snake_case_model_name}")
    @ns.marshal_with(${singular_pascal_case_model_name}PaginateResponse)
    @auth.login_required
    def get(self):
        return self.controller.get()

    @ns.doc("create_new_${singular_snake_case_model_name}")
    @ns.marshal_with(${singular_pascal_case_model_name}Response)
    @ns.expect(Create${singular_pascal_case_model_name}Request)
    @auth.login_required
    def post(self):
        data = api.payload
        return self.controller.create(data=data)


@ns.route('/<int:_id>')
@ns.param('_id', 'ID of ${singular_pascal_case_model_name}')
class ${singular_pascal_case_model_name}CommonRoute(BaseRoute):
    def get_controller(self):
        return ${singular_pascal_case_model_name}Controller

    @ns.doc('get_${singular_snake_case_model_name}_by_id')
    @ns.marshal_with(${singular_pascal_case_model_name}Response)
    @auth.login_required
    def get(self, _id):
        return self.controller.get(_id)

    @ns.doc("update_${singular_snake_case_model_name}_by_id")
    @ns.marshal_with(${singular_pascal_case_model_name}Response)
    @ns.expect(Update${singular_pascal_case_model_name}Request)
    @auth.login_required
    def put(self, _id):
        data = api.payload
        return self.controller.update(_id=_id, data=data)

    @ns.doc("delete_${singular_snake_case_model_name}_by_id")
    @auth.login_required
    def delete(self, _id):
        return self.controller.delete(_id=_id)
