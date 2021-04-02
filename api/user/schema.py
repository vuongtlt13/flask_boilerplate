from flask_restx import fields

from extensions import api
from extensions.response import PaginateResponseSchema, ResponseSchema, paginate_model

UserSchema = api.model('User', {
    'id': fields.Integer(readOnly=True, required=True),
    'service_id': fields.Integer(readOnly=False, required=True),
    'username': fields.String(readOnly=False, required=True),
    'password': fields.String(readOnly=False, required=True),
    'is_active': fields.Boolean(readOnly=False, required=True),
})

UserResponse = api.clone('UserResponse', ResponseSchema, {
    "data": fields.Nested(UserSchema, allow_null=True)
})

CreateUserRequest = api.model('CreateUserRequest', {
    'service_id': fields.Integer(readOnly=False, required=True),
    'username': fields.String(readOnly=False, required=True),
    'password': fields.String(readOnly=False, required=True),
    'is_active': fields.Boolean(readOnly=False, required=True),
})

UpdateUserRequest = api.model('UpdateUserRequest', {
    'service_id': fields.Integer(readOnly=False, required=True),
    'username': fields.String(readOnly=False, required=True),
    'password': fields.String(readOnly=False, required=True),
    'is_active': fields.Boolean(readOnly=False, required=True),
})

user_paginate_model = api.clone('user_paginate_model', paginate_model, {
    'users': fields.List(fields.Nested(UserSchema))
})

UserPaginateResponse = api.clone('UserPaginateResponse', PaginateResponseSchema, {
    'data': fields.Nested(user_paginate_model),
})
