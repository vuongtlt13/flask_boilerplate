from typing import Dict
from extensions.vgenerator.base import BaseGenerator
from extensions.vgenerator.model import ModelGenerator


class ControllerGenerator(BaseGenerator):
    def __init__(self, model: ModelGenerator):
        self.model_class_name = model.class_name
        self.table_name = model.table_name
        super().__init__(self.model_class_name)
        self.model = model

    def get_variables(self) -> Dict:
        return {
            "has_password_column": self.model.has_password_column,
            "password_columns": self.__render_password_columns(),
        }

    def template_file(self):
        return "controller.mako"

    def output_filename(self):
        return "controller"

    def __render_password_columns(self):
        lines = []
        for column in list(self.model.attributes.values()):
            if column.is_password_column:
                lines.append(column.column.name)
        return lines
