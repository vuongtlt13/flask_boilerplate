from flask_restx import fields

from extensions import api
from extensions.response import PaginateResponseSchema, ResponseSchema, paginate_model

LicenseOptionSchema = api.model('LicenseOption', {
    'id': fields.Integer(readOnly=True, required=True),
    'license_id': fields.Integer(readOnly=False, required=True),
    'option_id': fields.Integer(readOnly=False, required=True),
    'amount': fields.Integer(readOnly=False, required=True),
    'unit_price': fields.Integer(readOnly=False, required=True),
})

LicenseOptionResponse = api.clone('LicenseOptionResponse', ResponseSchema, {
    "data": fields.Nested(LicenseOptionSchema, allow_null=True)
})

CreateLicenseOptionRequest = api.model('CreateLicenseOptionRequest', {
    'license_id': fields.Integer(readOnly=False, required=True),
    'option_id': fields.Integer(readOnly=False, required=True),
    'amount': fields.Integer(readOnly=False, required=True),
    'unit_price': fields.Integer(readOnly=False, required=True),
})

UpdateLicenseOptionRequest = api.model('UpdateLicenseOptionRequest', {
    'license_id': fields.Integer(readOnly=False, required=True),
    'option_id': fields.Integer(readOnly=False, required=True),
    'amount': fields.Integer(readOnly=False, required=True),
    'unit_price': fields.Integer(readOnly=False, required=True),
})

license_option_paginate_model = api.clone('license_option_paginate_model', paginate_model, {
    'license_options': fields.List(fields.Nested(LicenseOptionSchema))
})

LicenseOptionPaginateResponse = api.clone('LicenseOptionPaginateResponse', PaginateResponseSchema, {
    'data': fields.Nested(license_option_paginate_model, allow_null=True),
})
