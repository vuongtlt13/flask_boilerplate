from flask_restx import fields

from extensions import api
from extensions.response import PaginateResponseSchema, ResponseSchema, paginate_model

LicenseTemplateSchema = api.model('LicenseTemplate', {
    'id': fields.Integer(readOnly=True, required=True),
    'name': fields.String(readOnly=False, required=True),
    'description': fields.String(readOnly=False, required=False),
})

LicenseTemplateResponse = api.clone('LicenseTemplateResponse', ResponseSchema, {
    "data": fields.Nested(LicenseTemplateSchema, allow_null=True)
})

CreateLicenseTemplateRequest = api.model('CreateLicenseTemplateRequest', {
    'name': fields.String(readOnly=False, required=True),
    'description': fields.String(readOnly=False, required=False),
})

UpdateLicenseTemplateRequest = api.model('UpdateLicenseTemplateRequest', {
    'name': fields.String(readOnly=False, required=True),
    'description': fields.String(readOnly=False, required=False),
})

license_template_paginate_model = api.clone('license_template_paginate_model', paginate_model, {
    'license_templates': fields.List(fields.Nested(LicenseTemplateSchema))
})

LicenseTemplatePaginateResponse = api.clone('LicenseTemplatePaginateResponse', PaginateResponseSchema, {
    'data': fields.Nested(license_template_paginate_model, allow_null=True),
})
