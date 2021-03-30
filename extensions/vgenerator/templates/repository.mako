<%include file="header.mako"/>

from api.core import BaseRepository
from api.${singular_snake_case_model_name}.model import ${model_class_name}


class ${singular_pascal_case_model_name}Repository(BaseRepository):
    def model(self):
        return ${model_class_name}
