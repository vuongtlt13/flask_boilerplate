"""
    Author: Do Quoc Vuong
    Email: vuongtlt13@gmail.com
    Country: VietNam
    Generated by VGenerator
    Created at: 2021-06-15 10:23:12.534453Z
"""

from typing import Dict
from flask import request
from api.core import BaseController, constants, utils
from api.option.repository import OptionRepository


class OptionController(BaseController):
    def __init__(self):
        super().__init__()
        self.option_repository = OptionRepository()

    def get(self, _id=None):
        if _id is not None:
            option = self.option_repository.find_by_id(_id)
            if option:
                option = option.as_dict()
            return self.success(data=option)

        args = request.args.to_dict()
        page = int(args.get('page', constants.DEFAULT_PAGE))
        size = int(args.get('size', constants.DEFAULT_PAGE_SIZE))
        options = self.option_repository.get(page=page, size=size)
        for index, option in enumerate(options):
            options[index] = option.as_dict()

        result = utils.paginate_serializer(page=page, size=size, data=options, data_key_name='options')
        return self.success(data=result)

    def create(self, data: Dict):
        new_option, errors = self.option_repository.create(data=data)
        if errors:
            return self.error(error=errors)

        return self.success(data=new_option.as_dict())

    def update(self, _id, data: Dict):

        option, errors = self.option_repository.update(_id, data=data)
        if errors:
            return self.error(error=errors)

        if option:
            option = option.as_dict()
        return self.success(data=option)

    def delete(self, _id):
        self.option_repository.delete(_id)
        return self.success(data=[])
