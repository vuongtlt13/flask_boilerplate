from flask_restx import fields

from extensions import api
from extensions.response import PaginateResponseSchema, ResponseSchema, paginate_model

DevelopDeviceSchema = api.model('DevelopDevice', {
    'id': fields.String(readOnly=True, required=True),
    'name': fields.String(readOnly=False, required=True),
    'ip_address': fields.String(readOnly=False, required=False),
    'country': fields.String(readOnly=False, required=False),
    'city': fields.String(readOnly=False, required=False),
})

DevelopDeviceResponse = api.clone('DevelopDeviceResponse', ResponseSchema, {
    "data": fields.Nested(DevelopDeviceSchema, allow_null=True)
})

CreateDevelopDeviceRequest = api.model('CreateDevelopDeviceRequest', {
    'name': fields.String(readOnly=False, required=True),
    'ip_address': fields.String(readOnly=False, required=False),
    'country': fields.String(readOnly=False, required=False),
    'city': fields.String(readOnly=False, required=False),
})

UpdateDevelopDeviceRequest = api.model('UpdateDevelopDeviceRequest', {
    'name': fields.String(readOnly=False, required=True),
    'ip_address': fields.String(readOnly=False, required=False),
    'country': fields.String(readOnly=False, required=False),
    'city': fields.String(readOnly=False, required=False),
})

develop_device_paginate_model = api.clone('develop_device_paginate_model', paginate_model, {
    'develop_devices': fields.List(fields.Nested(DevelopDeviceSchema))
})

DevelopDevicePaginateResponse = api.clone('DevelopDevicePaginateResponse', PaginateResponseSchema, {
    'data': fields.Nested(develop_device_paginate_model, allow_null=True),
})
