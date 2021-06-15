from flask_restx import fields

from extensions import api
from extensions.response import PaginateResponseSchema, ResponseSchema, paginate_model

ApplicationConfigSchema = api.model('ApplicationConfig', {
    'id': fields.Integer(readOnly=True, required=True),
    'application_id': fields.Integer(readOnly=False, required=True),
    'user_id': fields.Integer(readOnly=False, required=True),
    'config': fields.String(readOnly=False, required=False),
})

ApplicationConfigResponse = api.clone('ApplicationConfigResponse', ResponseSchema, {
    "data": fields.Nested(ApplicationConfigSchema, allow_null=True)
})

CreateApplicationConfigRequest = api.model('CreateApplicationConfigRequest', {
    'application_id': fields.Integer(readOnly=False, required=True),
    'user_id': fields.Integer(readOnly=False, required=True),
    'config': fields.String(readOnly=False, required=False),
})

UpdateApplicationConfigRequest = api.model('UpdateApplicationConfigRequest', {
    'application_id': fields.Integer(readOnly=False, required=True),
    'user_id': fields.Integer(readOnly=False, required=True),
    'config': fields.String(readOnly=False, required=False),
})

application_config_paginate_model = api.clone('application_config_paginate_model', paginate_model, {
    'application_configs': fields.List(fields.Nested(ApplicationConfigSchema))
})

ApplicationConfigPaginateResponse = api.clone('ApplicationConfigPaginateResponse', PaginateResponseSchema, {
    'data': fields.Nested(application_config_paginate_model, allow_null=True),
})
