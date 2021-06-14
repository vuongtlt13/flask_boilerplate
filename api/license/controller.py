"""
    Author: Do Quoc Vuong
    Email: vuongtlt13@gmail.com
    Country: VietNam
    Generated by VGenerator
    Created at: 2021-06-11 17:52:02.903799Z
"""

from typing import Dict
from flask import request
from api.core import BaseController, constants, utils
from api.license.repository import LicenseRepository


class LicenseController(BaseController):
    def __init__(self):
        super().__init__()
        self.license_repository = LicenseRepository()

    def get(self, _id=None):
        if _id is not None:
            license = self.license_repository.find_by_id(_id)
            if license:
                license = license.as_dict()
            return self.success(data=license)

        args = request.args.to_dict()
        page = int(args.get('page', constants.DEFAULT_PAGE))
        size = int(args.get('size', constants.DEFAULT_PAGE_SIZE))
        licenses = self.license_repository.get(page=page, size=size)
        for index, license in enumerate(licenses):
            licenses[index] = license.as_dict()

        result = utils.paginate_serializer(page=page, size=size, data=licenses, data_key_name='licenses')
        return self.success(data=result)

    def create(self, data: Dict):
        new_license, errors = self.license_repository.create(data=data)
        if errors:
            return self.error(error=errors)

        return self.success(data=new_license.as_dict())

    def update(self, _id, data: Dict):

        license, errors = self.license_repository.update(_id, data=data)
        if errors:
            return self.error(error=errors)

        if license:
            license = license.as_dict()
        return self.success(data=license)

    def delete(self, _id):
        self.license_repository.delete(_id)
        return self.success(data=[])