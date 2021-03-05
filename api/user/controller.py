from typing import Dict

from flask import request

from api.core import BaseController, constants, ultils
from api.user.repository import UserRepository


class UserController(BaseController):
    def __init__(self):
        super().__init__()
        self.user_repository = UserRepository()

    def get(self, id=None):
        if id is not None:
            user = self.user_repository.find_by_id(id)
            if user:
                user = user.as_dict()
            return self.success(data=user)

        args = request.args.to_dict()
        page = int(args.get('page', constants.DEFAULT_PAGE))
        size = int(args.get('size', constants.DEFAULT_PAGE_SIZE))
        users = self.user_repository.get(page=page, size=size)
        for index, user in enumerate(users):
            users[index] = user.as_dict()

        result = ultils.paginate_serializer(page=page, size=size, data=users, data_key_name='users')
        return self.success(data=result)

    def create(self, data: Dict):
        return self.success(data=self.user_repository.create(data=data).as_dict())

    def update(self, id, data: Dict):
        user = self.user_repository.update(id, data=data)
        if user:
            user = user.as_dict()
        return self.success(data=user)

    def delete(self, id):
        self.user_repository.delete(id)
        return self.success(data=[])
