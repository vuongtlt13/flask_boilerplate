<%include file="header.mako"/>

from typing import Dict
from flask import request
from api.core import BaseController, constants, utils
from api.${singular_snake_case_model_name}.repository import ${singular_pascal_case_model_name}Repository


class ${singular_pascal_case_model_name}Controller(BaseController):
    def __init__(self):
        super().__init__()
        self.${singular_snake_case_model_name}_repository = ${singular_pascal_case_model_name}Repository()

    def get(self, _id=None):
        if _id is not None:
            ${singular_snake_case_model_name} = self.${singular_snake_case_model_name}_repository.find_by_id(_id)
            if ${singular_snake_case_model_name}:
                ${singular_snake_case_model_name} = ${singular_snake_case_model_name}.as_dict()
            return self.success(data=${singular_snake_case_model_name})

        args = request.args.to_dict()
        page = int(args.get('page', constants.DEFAULT_PAGE))
        size = int(args.get('size', constants.DEFAULT_PAGE_SIZE))
        ${plural_snake_case_model_name} = self.${singular_snake_case_model_name}_repository.get(page=page, size=size)
        for index, ${singular_snake_case_model_name} in enumerate(${plural_snake_case_model_name}):
            ${plural_snake_case_model_name}[index] = ${singular_snake_case_model_name}.as_dict()

        result = utils.paginate_serializer(page=page, size=size, data=${plural_snake_case_model_name}, data_key_name='${plural_snake_case_model_name}')
        return self.success(data=result)

    def create(self, data: Dict):
        return self.success(data=self.${singular_snake_case_model_name}_repository.create(data=data).as_dict())

    def update(self, _id, data: Dict):
        ${singular_snake_case_model_name} = self.${singular_snake_case_model_name}_repository.update(_id, data=data)
        if ${singular_snake_case_model_name}:
            ${singular_snake_case_model_name} = ${singular_snake_case_model_name}.as_dict()
        return self.success(data=${singular_snake_case_model_name})

    def delete(self, _id):
        self.${singular_snake_case_model_name}_repository.delete(_id)
        return self.success(data=[])
