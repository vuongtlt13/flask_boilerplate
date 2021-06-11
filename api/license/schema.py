from flask_restx import fields

from extensions import api
from extensions.response import PaginateResponseSchema, ResponseSchema, paginate_model

LicenseSchema = api.model('License', {
    'id': fields.Integer(readOnly=True, required=True),
    'code': fields.String(readOnly=False, required=True),
    'application_id': fields.Integer(readOnly=False, required=True),
    'user_id': fields.Integer(readOnly=False, required=True),
    'is_active': fields.Integer(readOnly=False, required=True),
    'actived_at': fields.DateTime(readOnly=False, required=False),
    'expired_at': fields.DateTime(readOnly=False, required=False),
})

LicenseResponse = api.clone('LicenseResponse', ResponseSchema, {
    "data": fields.Nested(LicenseSchema, allow_null=True)
})

CreateLicenseRequest = api.model('CreateLicenseRequest', {
    'code': fields.String(readOnly=False, required=True),
    'application_id': fields.Integer(readOnly=False, required=True),
    'user_id': fields.Integer(readOnly=False, required=True),
    'is_active': fields.Integer(readOnly=False, required=True),
    'actived_at': fields.DateTime(readOnly=False, required=False),
    'expired_at': fields.DateTime(readOnly=False, required=False),
})

UpdateLicenseRequest = api.model('UpdateLicenseRequest', {
    'code': fields.String(readOnly=False, required=True),
    'application_id': fields.Integer(readOnly=False, required=True),
    'user_id': fields.Integer(readOnly=False, required=True),
    'is_active': fields.Integer(readOnly=False, required=True),
    'actived_at': fields.DateTime(readOnly=False, required=False),
    'expired_at': fields.DateTime(readOnly=False, required=False),
})

license_paginate_model = api.clone('license_paginate_model', paginate_model, {
    'licenses': fields.List(fields.Nested(LicenseSchema))
})

LicensePaginateResponse = api.clone('LicensePaginateResponse', PaginateResponseSchema, {
    'data': fields.Nested(license_paginate_model, allow_null=True),
})
