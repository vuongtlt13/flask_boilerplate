from flask_restx import fields

from extensions import api
from extensions.response import ResponseSchema

LoginSchema = api.model('LoginSchema', {
    'access_token': fields.String(readOnly=True, required=True),
})

LoginResponse = api.clone('LoginResponse', ResponseSchema, {
    "data": fields.Nested(LoginSchema, allow_null=True)
})

LoginRequest = api.model('LoginRequest', {
    'username': fields.String(readOnly=False, required=True),
    'password': fields.String(readOnly=False, required=True),
})
