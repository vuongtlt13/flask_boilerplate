from datetime import datetime, timedelta
from functools import wraps
from flask import request
from flask import current_app
import jwt

from api.user.model import User
from api.user.repository import UserRepository
from extensions.excpetion import AccessTokenExpired, AccessTokenInvalid, AccessTokenMissing


def get_access_token():
    if 'Authorization' not in request.headers:
        raise AccessTokenMissing("Token is missing")
    try:
        token = request.headers['Authorization'].split(" ")[-1]
        if not token:
            raise AccessTokenMissing("Token is missing")
    except:
        raise AccessTokenMissing("Token is missing")
    return token


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_access_token()
        decode_auth_token(token)
        return f(*args, **kwargs)

    return decorated


def encode_auth_token(user: User):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow(),
            'user': user.id,
        }
        return jwt.encode(
            payload,
            current_app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e


def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, current_app.config.get('SECRET_KEY'), algorithms='HS256')
        return payload
    except jwt.ExpiredSignatureError:
        raise AccessTokenExpired('Signature expired. Please log in again.')
    except jwt.InvalidTokenError:
        raise AccessTokenInvalid('Invalid token. Please log in again.')


def current_user():
    token = get_access_token()
    payload = decode_auth_token(token)
    user_id = payload['user']
    return UserRepository().find_by_id(user_id)
