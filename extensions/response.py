from flask_restx import fields

from extensions import api


def success(message="", data=None):
    resp_data = {
        'status': True,
        'data': data,
        'message': message,
        'error': None
    }
    return resp_data, 200


def error(message="", data=None, error=None, code: int = 400):
    resp_data = {
        'status': False,
        'data': data,
        'message': message,
        'error': error
    }

    return resp_data, code


ResponseSchema = api.model('ResponseSchema', {
    'status': fields.Boolean,
    'data': fields.Raw,
    'message': fields.String,
    'error': fields.String
})

paginate_model = api.model('paginate_model', {
    'page': fields.Integer,
    'size': fields.Integer,
})

PaginateResponseSchema = api.clone('PaginateResponseSchema', ResponseSchema, {
    'data': fields.Nested(paginate_model),
})
