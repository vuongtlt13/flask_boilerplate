from flask_restx import fields

from extensions import api


def success(data=None, message=""):
    resp_data = {
        'status': True,
        'data': data,
        'message': message
    }
    return resp_data, 200


def error(data=None, message: str = None, code: int = 400):
    resp_data = {
        'status': False,
        'data': data,
        'message': message
    }

    return resp_data, code


ResponseSchema = api.model('ResponseSchema', {
    'status': fields.Boolean,
    'data': fields.Raw,
    'message': fields.String
})

paginate_model = api.model('paginate_model', {
    'page': fields.Integer,
    'size': fields.Integer,
})

PaginateResponseSchema = api.clone('PaginateResponseSchema', ResponseSchema, {
    'data': fields.Nested(paginate_model),
})
