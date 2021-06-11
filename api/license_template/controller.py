"""
    Author: Do Quoc Vuong
    Email: vuongtlt13@gmail.com
    Country: VietNam
    Generated by VGenerator
    Created at: 2021-06-11 17:52:02.903579Z
"""

from typing import Dict
from flask import request
from api.core import BaseController, constants, utils
from api.license_template.repository import LicenseTemplateRepository


class LicenseTemplateController(BaseController):
    def __init__(self):
        super().__init__()
        self.license_template_repository = LicenseTemplateRepository()

    def get(self, _id=None):
        if _id is not None:
            license_template = self.license_template_repository.find_by_id(_id)
            if license_template:
                license_template = license_template.as_dict()
            return self.success(data=license_template)

        args = request.args.to_dict()
        page = int(args.get('page', constants.DEFAULT_PAGE))
        size = int(args.get('size', constants.DEFAULT_PAGE_SIZE))
        license_templates = self.license_template_repository.get(page=page, size=size)
        for index, license_template in enumerate(license_templates):
            license_templates[index] = license_template.as_dict()

        result = utils.paginate_serializer(page=page, size=size, data=license_templates, data_key_name='license_templates')
        return self.success(data=result)

    def create(self, data: Dict):
        new_license_template, errors = self.license_template_repository.create(data=data)
        if errors:
            return self.error(error=errors)

        return self.success(data=new_license_template.as_dict())

    def update(self, _id, data: Dict):

        license_template, errors = self.license_template_repository.update(_id, data=data)
        if errors:
            return self.error(error=errors)

        if license_template:
            license_template = license_template.as_dict()
        return self.success(data=license_template)

    def delete(self, _id):
        self.license_template_repository.delete(_id)
        return self.success(data=[])
