import os
from typing import Dict, List

from extensions.vgenerator.base import BaseGenerator
from extensions.vgenerator.model import ModelGenerator


class RouteGenerator(BaseGenerator):
    def __init__(self, model: ModelGenerator, main_route_file: str):
        self.model_class_name = model.class_name
        self.table_name = model.table_name
        self.main_route_file = main_route_file
        super().__init__(self.model_class_name)

    def get_variables(self) -> Dict:
        return {}

    def template_file(self):
        return "route.mako"

    def output_filename(self):
        return "route"

    def render(self, root_directory=".") -> str:
        super(RouteGenerator, self).render(root_directory=root_directory)
        self.update_main_route_file(root_directory)

    def update_main_route_file(self, root_directory: str):
        file_path = os.path.join(root_directory, self.main_route_file)
        lines = []
        with open(file_path, "r") as f:
            for line in f:
                lines.append(line)
            f.close()

        expected_line = self.generate_route_line()
        if expected_line not in lines:
            with open(file_path, "a") as f:
                f.write(expected_line)
                f.close()

    def generate_route_line(self):
        singular_snake_case_model_name = self._variables['singular_snake_case_model_name']
        return f'from .{singular_snake_case_model_name}.route import *\n'
