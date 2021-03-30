import datetime
import decimal
from typing import Dict, List, Optional

from extensions.vgenerator import utils
from extensions.vgenerator.base import BaseGenerator
from extensions.vgenerator.column import ColumnGenerator
from extensions.vgenerator.model import ModelGenerator


class SchemaColumn(BaseGenerator):
    def get_variables(self) -> Dict[str, str]:
        return {
            "column_name": self._column.column.name,
            "column_type": self.column_type,
            "column_options": self.column_option
        }

    def template_file(self):
        return "schema_column.mako"

    def output_filename(self):
        return None

    def __init__(self, column: ColumnGenerator, model_class_name: Optional[str]):
        super().__init__(model_class_name)
        self._column = column
        self.is_return = True
        is_creatable = (not self._column.is_primary and self._column.column.name not in utils.get_timestamps_columns())
        self.is_creatable = is_creatable
        self.is_updatable = is_creatable

    @property
    def python_type(self):
        column = self._column.column
        try:
            if hasattr(column.type, 'impl'):
                if hasattr(column.type.impl, 'python_type'):
                    return column.type.impl.python_type
                return type(column.type.impl)
            if hasattr(column.type, 'python_type'):
                return column.type.python_type
            return type(column.type)
        except Exception:  # pylint: disable=broad-except
            return type(column.type)

    @property
    def column_type(self):
        if self.python_type is int:
            return 'Integer'
        if self.python_type in [float, decimal.Decimal]:
            return 'Float'
        if self.python_type is bool:
            return 'Boolean'
        if self.python_type is datetime.datetime:
            return 'DateTime'
        if self.python_type is datetime.date:
            return 'Date'
        return 'String'

    @property
    def column_option(self):
        options = dict(
            readOnly=self._column.is_primary,
            required=not self._column.column.nullable
        )
        res = []
        for option_name, option_value in options.items():
            res.append(f"{option_name}={option_value}")
        return ", ".join(res)


class SchemaGenerator(BaseGenerator):
    def __init__(self, model: ModelGenerator):
        self.model_class_name = model.class_name
        self.table_name = model.table_name
        super().__init__(self.model_class_name)
        self.schema_columns: List[SchemaColumn] = []
        self.__init_schema_columns(model)

    def get_variables(self) -> Dict:
        return {
            "creatable_columns": self.__render_creatable_columns(),
            "updatable_columns": self.__render_updatable_columns(),
            "return_columns": self.__render_return_columns(),
        }

    def template_file(self):
        return "schema.mako"

    def output_filename(self):
        return "schema"

    def __render_return_columns(self):
        return [column.render() for column in self.schema_columns if column.is_return]

    def __init_schema_columns(self, model: ModelGenerator):
        for column_name, column in model.attributes.items():
            self.schema_columns.append(SchemaColumn(column, None))

    def __render_creatable_columns(self):
        return [column.render() for column in self.schema_columns if column.is_creatable]

    def __render_updatable_columns(self):
        return [column.render() for column in self.schema_columns if column.is_updatable]
