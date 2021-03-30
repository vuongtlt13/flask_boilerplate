from typing import Dict

from extensions.vgenerator.base import BaseGenerator
from extensions.vgenerator.model import ModelGenerator


class RepositoryGenerator(BaseGenerator):
    def __init__(self, model: ModelGenerator):
        self.model_class_name = model.class_name
        self.table_name = model.table_name
        super().__init__(self.model_class_name)

    def get_variables(self) -> Dict:
        return {}

    def template_file(self):
        return "repository.mako"

    def output_filename(self):
        return "repository"
