from flask_restx import fields

from extensions import api
from extensions.response import PaginateResponseSchema, ResponseSchema, paginate_model

OptionSchema = api.model('Option', {
    'id': fields.Integer(readOnly=True, required=True),
    'name': fields.String(readOnly=False, required=True),
    'description': fields.String(readOnly=False, required=True),
    'unit_price': fields.Integer(readOnly=False, required=True),
    'unit_amount': fields.Integer(readOnly=False, required=True),
})

OptionResponse = api.clone('OptionResponse', ResponseSchema, {
    "data": fields.Nested(OptionSchema, allow_null=True)
})

CreateOptionRequest = api.model('CreateOptionRequest', {
    'name': fields.String(readOnly=False, required=True),
    'description': fields.String(readOnly=False, required=True),
    'unit_price': fields.Integer(readOnly=False, required=True),
    'unit_amount': fields.Integer(readOnly=False, required=True),
})

UpdateOptionRequest = api.model('UpdateOptionRequest', {
    'name': fields.String(readOnly=False, required=True),
    'description': fields.String(readOnly=False, required=True),
    'unit_price': fields.Integer(readOnly=False, required=True),
    'unit_amount': fields.Integer(readOnly=False, required=True),
})

option_paginate_model = api.clone('option_paginate_model', paginate_model, {
    'options': fields.List(fields.Nested(OptionSchema))
})

OptionPaginateResponse = api.clone('OptionPaginateResponse', PaginateResponseSchema, {
    'data': fields.Nested(option_paginate_model, allow_null=True),
})
