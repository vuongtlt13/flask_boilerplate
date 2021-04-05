from flask_restx import fields

from extensions import api
from extensions.response import PaginateResponseSchema, ResponseSchema, paginate_model

AppSchema = api.model('App', {
    'id': fields.Integer(readOnly=True, required=True),
    'name': fields.String(readOnly=False, required=True),
})

AppResponse = api.clone('AppResponse', ResponseSchema, {
    "data": fields.Nested(AppSchema, allow_null=True)
})

CreateAppRequest = api.model('CreateAppRequest', {
    'name': fields.String(readOnly=False, required=True),
})

UpdateAppRequest = api.model('UpdateAppRequest', {
    'name': fields.String(readOnly=False, required=True),
})

app_paginate_model = api.clone('app_paginate_model', paginate_model, {
    'apps': fields.List(fields.Nested(AppSchema))
})

AppPaginateResponse = api.clone('AppPaginateResponse', PaginateResponseSchema, {
    'data': fields.Nested(app_paginate_model, allow_null=True),
})
