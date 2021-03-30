"""
    Author: Do Quoc Vuong
    Email: vuongtlt13@gmail.com
    Country: VietNam
    Generated by VGenerator
    Created at: 2021-03-30 04:03:36.843039Z
"""

from typing import Dict
from flask import request
from api.core import BaseController, constants, utils
from api.company.repository import CompanyRepository


class CompanyController(BaseController):
    def __init__(self):
        super().__init__()
        self.company_repository = CompanyRepository()

    def get(self, _id=None):
        if _id is not None:
            company = self.company_repository.find_by_id(_id)
            if company:
                company = company.as_dict()
            return self.success(data=company)

        args = request.args.to_dict()
        page = int(args.get('page', constants.DEFAULT_PAGE))
        size = int(args.get('size', constants.DEFAULT_PAGE_SIZE))
        companies = self.company_repository.get(page=page, size=size)
        for index, company in enumerate(companies):
            companies[index] = company.as_dict()

        result = utils.paginate_serializer(page=page, size=size, data=companies, data_key_name='companies')
        return self.success(data=result)

    def create(self, data: Dict):
        return self.success(data=self.company_repository.create(data=data).as_dict())

    def update(self, _id, data: Dict):
        company = self.company_repository.update(_id, data=data)
        if company:
            company = company.as_dict()
        return self.success(data=company)

    def delete(self, _id):
        self.company_repository.delete(_id)
        return self.success(data=[])
