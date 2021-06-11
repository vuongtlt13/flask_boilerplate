"""
    Author: Do Quoc Vuong
    Email: vuongtlt13@gmail.com
    Country: VietNam
    Generated by VGenerator
    Created at: 2021-06-11 17:52:02.902530Z
"""

from typing import Dict
from flask import request
from api.core import BaseController, constants, utils
from api.application.repository import ApplicationRepository


class ApplicationController(BaseController):
    def __init__(self):
        super().__init__()
        self.application_repository = ApplicationRepository()

    def get(self, _id=None):
        if _id is not None:
            application = self.application_repository.find_by_id(_id)
            if application:
                application = application.as_dict()
            return self.success(data=application)

        args = request.args.to_dict()
        page = int(args.get('page', constants.DEFAULT_PAGE))
        size = int(args.get('size', constants.DEFAULT_PAGE_SIZE))
        applications = self.application_repository.get(page=page, size=size)
        for index, application in enumerate(applications):
            applications[index] = application.as_dict()

        result = utils.paginate_serializer(page=page, size=size, data=applications, data_key_name='applications')
        return self.success(data=result)

    def create(self, data: Dict):
        new_application, errors = self.application_repository.create(data=data)
        if errors:
            return self.error(error=errors)

        return self.success(data=new_application.as_dict())

    def update(self, _id, data: Dict):

        application, errors = self.application_repository.update(_id, data=data)
        if errors:
            return self.error(error=errors)

        if application:
            application = application.as_dict()
        return self.success(data=application)

    def delete(self, _id):
        self.application_repository.delete(_id)
        return self.success(data=[])
