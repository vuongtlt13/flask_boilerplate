from flask_restx import fields

from extensions import api
from extensions.response import PaginateResponseSchema, ResponseSchema, paginate_model

ApplicationSchema = api.model('Application', {
    'id': fields.Integer(readOnly=True, required=True),
    'name': fields.String(readOnly=False, required=True),
    'code': fields.String(readOnly=False, required=True),
    'description': fields.String(readOnly=False, required=True),
})

ApplicationResponse = api.clone('ApplicationResponse', ResponseSchema, {
    "data": fields.Nested(ApplicationSchema, allow_null=True)
})

CreateApplicationRequest = api.model('CreateApplicationRequest', {
    'name': fields.String(readOnly=False, required=True),
    'code': fields.String(readOnly=False, required=True),
    'description': fields.String(readOnly=False, required=True),
})

UpdateApplicationRequest = api.model('UpdateApplicationRequest', {
    'name': fields.String(readOnly=False, required=True),
    'code': fields.String(readOnly=False, required=True),
    'description': fields.String(readOnly=False, required=True),
})

application_paginate_model = api.clone('application_paginate_model', paginate_model, {
    'applications': fields.List(fields.Nested(ApplicationSchema))
})

ApplicationPaginateResponse = api.clone('ApplicationPaginateResponse', PaginateResponseSchema, {
    'data': fields.Nested(application_paginate_model, allow_null=True),
})
