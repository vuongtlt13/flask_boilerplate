"""
    Author: Do Quoc Vuong
    Email: vuongtlt13@gmail.com
    Country: VietNam
    Generated by VGenerator
    Created at: 2021-06-10 04:00:03.701927Z
"""

from typing import Dict
from flask import request
from api.core import BaseController, constants, utils
from werkzeug.security import generate_password_hash
from api.user.repository import UserRepository


class UserController(BaseController):
    def __init__(self):
        super().__init__()
        self.user_repository = UserRepository()

    def get(self, _id=None):
        if _id is not None:
            user = self.user_repository.find_by_id(_id)
            if user:
                user = user.as_dict()
            return self.success(data=user)

        args = request.args.to_dict()
        page = int(args.get('page', constants.DEFAULT_PAGE))
        size = int(args.get('size', constants.DEFAULT_PAGE_SIZE))
        users = self.user_repository.get(page=page, size=size)
        for index, user in enumerate(users):
            users[index] = user.as_dict()

        result = utils.paginate_serializer(page=page, size=size, data=users, data_key_name='users')
        return self.success(data=result)

    def create(self, data: Dict):
        data['password'] = generate_password_hash(data['password'])
        new_user, errors = self.user_repository.create(data=data)
        if errors:
            return self.error(error=errors)

        return self.success(data=new_user.as_dict())

    def update(self, _id, data: Dict):
        password = data.get('password', None)
        if password:
            data['password'] = generate_password_hash(data['password'])
        else:
            data.pop('password', None)

        user, errors = self.user_repository.update(_id, data=data)
        if errors:
            return self.error(error=errors)

        if user:
            user = user.as_dict()
        return self.success(data=user)

    def delete(self, _id):
        self.user_repository.delete(_id)
        return self.success(data=[])
