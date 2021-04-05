from flask_restx import fields

from extensions import api
from extensions.response import PaginateResponseSchema, ResponseSchema, paginate_model

ServiceSchema = api.model('Service', {
    'id': fields.Integer(readOnly=True, required=True),
    'app_id': fields.Integer(readOnly=False, required=True),
    'company_id': fields.Integer(readOnly=False, required=True),
    'is_active': fields.Boolean(readOnly=False, required=True),
})

ServiceResponse = api.clone('ServiceResponse', ResponseSchema, {
    "data": fields.Nested(ServiceSchema, allow_null=True)
})

CreateServiceRequest = api.model('CreateServiceRequest', {
    'app_id': fields.Integer(readOnly=False, required=True),
    'company_id': fields.Integer(readOnly=False, required=True),
    'is_active': fields.Boolean(readOnly=False, required=True),
})

UpdateServiceRequest = api.model('UpdateServiceRequest', {
    'app_id': fields.Integer(readOnly=False, required=True),
    'company_id': fields.Integer(readOnly=False, required=True),
    'is_active': fields.Boolean(readOnly=False, required=True),
})

service_paginate_model = api.clone('service_paginate_model', paginate_model, {
    'services': fields.List(fields.Nested(ServiceSchema))
})

ServicePaginateResponse = api.clone('ServicePaginateResponse', PaginateResponseSchema, {
    'data': fields.Nested(service_paginate_model, allow_null=True),
})
