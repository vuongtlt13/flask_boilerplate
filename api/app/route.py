from api.core import auth
from api.core.route import BaseRoute
from api.app.controller import AppController
from api.app.schema import CreateAppRequest, UpdateAppRequest, AppPaginateResponse, AppResponse
from extensions import api

ns = api.namespace('apps', description='App operations')

__all__ = [
    "CreateAppRoute",
    "AppCommonRoute"
]


@ns.route('')
class CreateAppRoute(BaseRoute):
    def get_controller(self):
        return AppController

    @ns.doc("list_apps")
    @ns.marshal_with(AppPaginateResponse)
    @auth.login_required
    def get(self):
        return self.controller.get()

    @ns.doc("create_new_app")
    @ns.marshal_with(AppResponse)
    @ns.expect(CreateAppRequest)
    @auth.login_required
    def post(self):
        data = api.payload
        return self.controller.create(data=data)


@ns.route('/<int:_id>')
@ns.param('_id', 'ID of App')
class AppCommonRoute(BaseRoute):
    def get_controller(self):
        return AppController

    @ns.doc('get_app_by_id')
    @ns.marshal_with(AppResponse)
    @auth.login_required
    def get(self, _id):
        return self.controller.get(_id)

    @ns.doc("update_app_by_id")
    @ns.marshal_with(AppResponse)
    @ns.expect(UpdateAppRequest)
    @auth.login_required
    def put(self, _id):
        data = api.payload
        return self.controller.update(_id=_id, data=data)

    @ns.doc("delete_app_by_id")
    @auth.login_required
    def delete(self, _id):
        return self.controller.delete(_id=_id)
