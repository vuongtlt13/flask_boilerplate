from flask_restx import fields

from extensions import api
from extensions.response import PaginateResponseSchema, ResponseSchema, paginate_model

UserProfileSchema = api.model('UserProfile', {
    'user_id': fields.Integer(readOnly=True, required=True),
    'tax_code': fields.String(readOnly=False, required=False),
    'bank_number': fields.String(readOnly=False, required=False),
    'bank_name': fields.String(readOnly=False, required=False),
})

UserProfileResponse = api.clone('UserProfileResponse', ResponseSchema, {
    "data": fields.Nested(UserProfileSchema, allow_null=True)
})

CreateUserProfileRequest = api.model('CreateUserProfileRequest', {
    'tax_code': fields.String(readOnly=False, required=False),
    'bank_number': fields.String(readOnly=False, required=False),
    'bank_name': fields.String(readOnly=False, required=False),
})

UpdateUserProfileRequest = api.model('UpdateUserProfileRequest', {
    'tax_code': fields.String(readOnly=False, required=False),
    'bank_number': fields.String(readOnly=False, required=False),
    'bank_name': fields.String(readOnly=False, required=False),
})

user_profile_paginate_model = api.clone('user_profile_paginate_model', paginate_model, {
    'user_profiles': fields.List(fields.Nested(UserProfileSchema))
})

UserProfilePaginateResponse = api.clone('UserProfilePaginateResponse', PaginateResponseSchema, {
    'data': fields.Nested(user_profile_paginate_model, allow_null=True),
})
