import abc
import os
from typing import Dict, Optional

import inflection
from mako.lookup import TemplateLookup
from mako.template import Template

from extensions.vgenerator import utils


TEMPLATE_DIRECTORY = "extensions/vgenerator/templates/"


class BaseGenerator(object):
    def __init__(self, model_class_name: Optional[str]):
        self.class_name = model_class_name
        self._variables: Dict[str, str] = {}
        if model_class_name:
            self.__generate_common_variables(model_class_name)

    @abc.abstractmethod
    def get_variables(self) -> Dict[str, str]:
        raise NotImplemented

    def template_path(self):
        return os.path.join(TEMPLATE_DIRECTORY, self.template_file())

    @abc.abstractmethod
    def template_file(self):
        raise NotImplemented

    @abc.abstractmethod
    def output_filename(self):
        raise NotImplemented

    def get_outfile(self, root_directory: str, class_name: str):
        if self.output_filename():
            directory = f'{root_directory}/{inflection.underscore(class_name)}'
            file_path = f"{directory}/{self.output_filename()}.py"
            if not os.path.exists(directory):
                os.mkdir(directory)
            return open(file_path, 'w+', encoding='utf8')
        return None

    def render(self, root_directory=".") -> str:
        outfile = self.get_outfile(root_directory=root_directory, class_name=self.class_name)
        variables = {
            **self._variables,
            **self.get_variables()
        }
        my_lookup = TemplateLookup(directories=["."])
        template = Template(filename=self.template_path(), lookup=my_lookup)
        res = template.render(**variables).rstrip("\n")
        if outfile:
            print(res, file=outfile)
            outfile.close()
        return res

    def __generate_common_variables(self, model_class_name: str):
        self._variables['datetime_now'] = utils.get_datetime_now()
        self._variables['model_class_name'] = model_class_name  # model_class_name in PascalCase

        self.__generate_singular_part(model_class_name)
        self.__generate_plural_part(model_class_name)

    def __generate_singular_part(self, model_class_name: str):
        self._variables['singular_snake_case_model_name'] = inflection.singularize(
            inflection.underscore(model_class_name))
        self._variables['singular_camel_case_model_name'] = inflection.singularize(
            inflection.camelize(model_class_name, False))
        self._variables['singular_pascal_case_model_name'] = inflection.singularize(model_class_name)

    def __generate_plural_part(self, model_class_name: str):
        self._variables['plural_snake_case_model_name'] = inflection.pluralize(
            inflection.underscore(model_class_name))
        self._variables['plural_camel_case_model_name'] = inflection.pluralize(
            inflection.camelize(model_class_name, False))
        self._variables['plural_pascal_case_model_name'] = inflection.pluralize(model_class_name)
