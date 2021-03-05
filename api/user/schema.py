from flask_restx import fields

from extensions import api
from extensions.response import PaginateResponseSchema, ResponseSchema, paginate_model

UserSchema = api.model('User', {
    'id': fields.Integer(readonly=True, description='The user unique identifier'),
    'username': fields.String(required=True, description='Username of user'),
    'created_at': fields.DateTime(description='Created at'),
    'updated_at': fields.DateTime(description='Updated at')
})

UserResponse = api.clone('UserResponse', ResponseSchema, {
    "data": fields.Nested(UserSchema)
})

CreateUserRequest = api.model('CreateUserRequest', {
    'username': fields.String(required=True, description='Username of user'),
    'password': fields.String(required=True, description='Password of user'),
})

UpdateUserRequest = api.model('UpdateUserRequest', {
    'password': fields.String(required=True, description='Password of user'),
})

user_paginate_model = api.clone('user_paginate_model', paginate_model, {
    'users': fields.List(fields.Nested(UserSchema))
})

UserPaginateResponse = api.clone('UserPaginateResponse', PaginateResponseSchema, {
    'data': fields.Nested(user_paginate_model),
})
