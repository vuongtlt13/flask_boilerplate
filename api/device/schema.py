from flask_restx import fields

from extensions import api
from extensions.response import PaginateResponseSchema, ResponseSchema, paginate_model

DeviceSchema = api.model('Device', {
    'id': fields.String(readOnly=True, required=True),
    'license_id': fields.Integer(readOnly=False, required=True),
    'name': fields.String(readOnly=False, required=False),
    'ip_address': fields.String(readOnly=False, required=False),
    'country': fields.String(readOnly=False, required=False),
    'city': fields.String(readOnly=False, required=False),
    'last_active_at': fields.DateTime(readOnly=False, required=False),
    'device_info': fields.String(readOnly=False, required=False),
})

DeviceResponse = api.clone('DeviceResponse', ResponseSchema, {
    "data": fields.Nested(DeviceSchema, allow_null=True)
})

CreateDeviceRequest = api.model('CreateDeviceRequest', {
    'license_id': fields.Integer(readOnly=False, required=True),
    'name': fields.String(readOnly=False, required=False),
    'ip_address': fields.String(readOnly=False, required=False),
    'country': fields.String(readOnly=False, required=False),
    'city': fields.String(readOnly=False, required=False),
    'last_active_at': fields.DateTime(readOnly=False, required=False),
    'device_info': fields.String(readOnly=False, required=False),
})

UpdateDeviceRequest = api.model('UpdateDeviceRequest', {
    'license_id': fields.Integer(readOnly=False, required=True),
    'name': fields.String(readOnly=False, required=False),
    'ip_address': fields.String(readOnly=False, required=False),
    'country': fields.String(readOnly=False, required=False),
    'city': fields.String(readOnly=False, required=False),
    'last_active_at': fields.DateTime(readOnly=False, required=False),
    'device_info': fields.String(readOnly=False, required=False),
})

device_paginate_model = api.clone('device_paginate_model', paginate_model, {
    'devices': fields.List(fields.Nested(DeviceSchema))
})

DevicePaginateResponse = api.clone('DevicePaginateResponse', PaginateResponseSchema, {
    'data': fields.Nested(device_paginate_model, allow_null=True),
})
