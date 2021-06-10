from flask_restx import fields

from extensions import api
from extensions.response import PaginateResponseSchema, ResponseSchema, paginate_model

UserSchema = api.model('User', {
    'id': fields.Integer(readOnly=True, required=True),
    'email': fields.String(readOnly=False, required=True),
    'password': fields.String(readOnly=False, required=True),
    'is_active': fields.Integer(readOnly=False, required=True),
})

UserResponse = api.clone('UserResponse', ResponseSchema, {
    "data": fields.Nested(UserSchema, allow_null=True)
})

CreateUserRequest = api.model('CreateUserRequest', {
    'email': fields.String(readOnly=False, required=True),
    'password': fields.String(readOnly=False, required=True),
    'is_active': fields.Integer(readOnly=False, required=True),
})

UpdateUserRequest = api.model('UpdateUserRequest', {
    'email': fields.String(readOnly=False, required=True),
    'password': fields.String(readOnly=False, required=True),
    'is_active': fields.Integer(readOnly=False, required=True),
})

user_paginate_model = api.clone('user_paginate_model', paginate_model, {
    'users': fields.List(fields.Nested(UserSchema))
})

UserPaginateResponse = api.clone('UserPaginateResponse', PaginateResponseSchema, {
    'data': fields.Nested(user_paginate_model, allow_null=True),
})
