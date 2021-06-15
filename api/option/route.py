from api.core.middlewares.token_verify import TokenVerify
from api.core.route import BaseRoute
from api.option.controller import OptionController
from api.option.schema import CreateOptionRequest, UpdateOptionRequest, OptionPaginateResponse, OptionResponse
from extensions import api, middleware_manager

ns = api.namespace('options', description='Option operations')

__all__ = [
    "CreateOptionRoute",
    "OptionCommonRoute"
]


@ns.route('')
@middleware_manager.route_middleware(TokenVerify)
class CreateOptionRoute(BaseRoute):
    def get_controller(self):
        return OptionController

    @ns.doc("list_options")
    @ns.marshal_with(OptionPaginateResponse)
    def get(self):
        return self.controller.get()

    @ns.doc("create_new_option")
    @ns.marshal_with(OptionResponse)
    @ns.expect(CreateOptionRequest)
    def post(self):
        data = api.payload
        return self.controller.create(data=data)


@ns.route('/<int:_id>')
@ns.param('_id', 'ID of Option')
@middleware_manager.route_middleware(TokenVerify)
class OptionCommonRoute(BaseRoute):
    def get_controller(self):
        return OptionController

    @ns.doc('get_option_by_id')
    @ns.marshal_with(OptionResponse)
    def get(self, _id):
        return self.controller.get(_id)

    @ns.doc("update_option_by_id")
    @ns.marshal_with(OptionResponse)
    @ns.expect(UpdateOptionRequest)
    def put(self, _id):
        data = api.payload
        return self.controller.update(_id=_id, data=data)

    @ns.doc("delete_option_by_id")
    def delete(self, _id):
        return self.controller.delete(_id=_id)
