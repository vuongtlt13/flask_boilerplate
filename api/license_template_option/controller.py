"""
    Author: Do Quoc Vuong
    Email: vuongtlt13@gmail.com
    Country: VietNam
    Generated by VGenerator
    Created at: 2021-06-15 10:23:12.533802Z
"""

from typing import Dict
from flask import request
from api.core import BaseController, constants, utils
from api.license_template_option.repository import LicenseTemplateOptionRepository


class LicenseTemplateOptionController(BaseController):
    def __init__(self):
        super().__init__()
        self.license_template_option_repository = LicenseTemplateOptionRepository()

    def get(self, _id=None):
        if _id is not None:
            license_template_option = self.license_template_option_repository.find_by_id(_id)
            if license_template_option:
                license_template_option = license_template_option.as_dict()
            return self.success(data=license_template_option)

        args = request.args.to_dict()
        page = int(args.get('page', constants.DEFAULT_PAGE))
        size = int(args.get('size', constants.DEFAULT_PAGE_SIZE))
        license_template_options = self.license_template_option_repository.get(page=page, size=size)
        for index, license_template_option in enumerate(license_template_options):
            license_template_options[index] = license_template_option.as_dict()

        result = utils.paginate_serializer(page=page, size=size, data=license_template_options, data_key_name='license_template_options')
        return self.success(data=result)

    def create(self, data: Dict):
        new_license_template_option, errors = self.license_template_option_repository.create(data=data)
        if errors:
            return self.error(error=errors)

        return self.success(data=new_license_template_option.as_dict())

    def update(self, _id, data: Dict):

        license_template_option, errors = self.license_template_option_repository.update(_id, data=data)
        if errors:
            return self.error(error=errors)

        if license_template_option:
            license_template_option = license_template_option.as_dict()
        return self.success(data=license_template_option)

    def delete(self, _id):
        self.license_template_option_repository.delete(_id)
        return self.success(data=[])
