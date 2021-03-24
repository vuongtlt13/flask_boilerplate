"""
    Author: Do Quoc Vuong
    Email: vuongtlt13@gmail.com
    Country: VietNam
    Generated by VGenerator
    Created at: 2021-03-24 11:06:07.075071Z
"""

from typing import Dict
from flask import request
from api.core import BaseController, constants, utils
from api.service.repository import ServiceRepository


class ServiceController(BaseController):
    def __init__(self):
        super().__init__()
        self.service_repository = ServiceRepository()

    def get(self, _id=None):
        if _id is not None:
            service = self.service_repository.find_by_id(_id)
            if service:
                service = service.as_dict()
            return self.success(data=service)

        args = request.args.to_dict()
        page = int(args.get('page', constants.DEFAULT_PAGE))
        size = int(args.get('size', constants.DEFAULT_PAGE_SIZE))
        services = self.service_repository.get(page=page, size=size)
        for index, service in enumerate(services):
            services[index] = service.as_dict()

        result = utils.paginate_serializer(page=page, size=size, data=services, data_key_name='services')
        return self.success(data=result)

    def create(self, data: Dict):
        return self.success(data=self.service_repository.create(data=data).as_dict())

    def update(self, _id, data: Dict):
        service = self.service_repository.update(_id, data=data)
        if service:
            service = service.as_dict()
        return self.success(data=service)

    def delete(self, _id):
        self.service_repository.delete(_id)
        return self.success(data=[])