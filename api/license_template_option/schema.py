from flask_restx import fields

from extensions import api
from extensions.response import PaginateResponseSchema, ResponseSchema, paginate_model

LicenseTemplateOptionSchema = api.model('LicenseTemplateOption', {
    'license_template_id': fields.Integer(readOnly=True, required=True),
    'option_id': fields.Integer(readOnly=True, required=True),
    'amount': fields.Integer(readOnly=False, required=True),
    'unit_price': fields.Integer(readOnly=False, required=True),
})

LicenseTemplateOptionResponse = api.clone('LicenseTemplateOptionResponse', ResponseSchema, {
    "data": fields.Nested(LicenseTemplateOptionSchema, allow_null=True)
})

CreateLicenseTemplateOptionRequest = api.model('CreateLicenseTemplateOptionRequest', {
    'amount': fields.Integer(readOnly=False, required=True),
    'unit_price': fields.Integer(readOnly=False, required=True),
})

UpdateLicenseTemplateOptionRequest = api.model('UpdateLicenseTemplateOptionRequest', {
    'amount': fields.Integer(readOnly=False, required=True),
    'unit_price': fields.Integer(readOnly=False, required=True),
})

license_template_option_paginate_model = api.clone('license_template_option_paginate_model', paginate_model, {
    'license_template_options': fields.List(fields.Nested(LicenseTemplateOptionSchema))
})

LicenseTemplateOptionPaginateResponse = api.clone('LicenseTemplateOptionPaginateResponse', PaginateResponseSchema, {
    'data': fields.Nested(license_template_option_paginate_model, allow_null=True),
})
