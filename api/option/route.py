from flask_jwt_extended import jwt_required
from api.core.route import BaseRoute
from api.option.controller import OptionController
from api.option.schema import CreateOptionRequest, UpdateOptionRequest, OptionPaginateResponse, OptionResponse
from extensions import api

ns = api.namespace('options', description='Option operations')

__all__ = [
    "CreateOptionRoute",
    "OptionCommonRoute"
]


@ns.route('')
class CreateOptionRoute(BaseRoute):
    def get_controller(self):
        return OptionController

    @ns.doc("list_options")
    @ns.marshal_with(OptionPaginateResponse)
    @jwt_required()
    def get(self):
        return self.controller.get()

    @ns.doc("create_new_option")
    @ns.marshal_with(OptionResponse)
    @ns.expect(CreateOptionRequest)
    @jwt_required()
    def post(self):
        data = api.payload
        return self.controller.create(data=data)


@ns.route('/<int:_id>')
@ns.param('_id', 'ID of Option')
class OptionCommonRoute(BaseRoute):
    def get_controller(self):
        return OptionController

    @ns.doc('get_option_by_id')
    @ns.marshal_with(OptionResponse)
    @jwt_required()
    def get(self, _id):
        return self.controller.get(_id)

    @ns.doc("update_option_by_id")
    @ns.marshal_with(OptionResponse)
    @ns.expect(UpdateOptionRequest)
    @jwt_required()
    def put(self, _id):
        data = api.payload
        return self.controller.update(_id=_id, data=data)

    @ns.doc("delete_option_by_id")
    @jwt_required()
    def delete(self, _id):
        return self.controller.delete(_id=_id)
