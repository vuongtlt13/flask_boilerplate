import json
from flask import make_response


def success(message="", data=None):
    resp = make_response(
        json.dumps({
            'status': True,
            'data': data,
            'message': message
        }),
        200
    )
    return resp


def error(message="", data=None, error=None, code: int = 400):
    resp = make_response(
        json.dumps({
            'status': False,
            'data': data,
            'message': message,
            'error': error
        }),
        code
    )
    return resp
