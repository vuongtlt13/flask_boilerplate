"""
    Author: Do Quoc Vuong
    Email: vuongtlt13@gmail.com
    Country: VietNam
    Generated by VGenerator
    Created at: 2021-06-15 10:23:12.534625Z
"""

from typing import Dict
from flask import request
from api.core import BaseController, constants, utils
from api.user_profile.repository import UserProfileRepository


class UserProfileController(BaseController):
    def __init__(self):
        super().__init__()
        self.user_profile_repository = UserProfileRepository()

    def get(self, _id=None):
        if _id is not None:
            user_profile = self.user_profile_repository.find_by_id(_id)
            if user_profile:
                user_profile = user_profile.as_dict()
            return self.success(data=user_profile)

        args = request.args.to_dict()
        page = int(args.get('page', constants.DEFAULT_PAGE))
        size = int(args.get('size', constants.DEFAULT_PAGE_SIZE))
        user_profiles = self.user_profile_repository.get(page=page, size=size)
        for index, user_profile in enumerate(user_profiles):
            user_profiles[index] = user_profile.as_dict()

        result = utils.paginate_serializer(page=page, size=size, data=user_profiles, data_key_name='user_profiles')
        return self.success(data=result)

    def create(self, data: Dict):
        new_user_profile, errors = self.user_profile_repository.create(data=data)
        if errors:
            return self.error(error=errors)

        return self.success(data=new_user_profile.as_dict())

    def update(self, _id, data: Dict):

        user_profile, errors = self.user_profile_repository.update(_id, data=data)
        if errors:
            return self.error(error=errors)

        if user_profile:
            user_profile = user_profile.as_dict()
        return self.success(data=user_profile)

    def delete(self, _id):
        self.user_profile_repository.delete(_id)
        return self.success(data=[])
