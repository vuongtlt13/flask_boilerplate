import os
import sys
from collections import defaultdict
from typing import Dict, List

from mako.template import Template
from sqlalchemy import ForeignKeyConstraint

from extensions.vgenerator import utils
from extensions.vgenerator.controller import ControllerGenerator
from extensions.vgenerator.model import ModelGenerator


class CodeGenerator(object):
    def __init__(self, metadata,
                 tables: List[str] = None,
                 ignore_tables: List[str] = None,
                 class_names: Dict = None,
                 ignore_cols=None,
                 no_comments=False,
                 ):
        """

        Args:
            metadata:
            tables:
            ignore_tables:
            class_names:
            ignore_cols:
            no_comments:
        """
        super(CodeGenerator, self).__init__()

        # exclude these column names from consideration when generating association tables
        self.class_names = class_names if class_names else {}
        self.ignore_tables = ignore_tables if ignore_tables else []
        self.ignore_tables = list(set(self.ignore_tables + ['alembic_version']))
        self.tables = tables
        self.metadata = metadata
        self._ignore_columns = ignore_cols or [] + utils.get_timestamps_columns()

        self.no_comments = no_comments

        self.association_tables = defaultdict(lambda: [])
        self.__init_association_tables()

        # Iterate through the tables and create model classes when possible
        self.models: List[ModelGenerator] = []
        self.__init_models()

        self.controllers: List[ControllerGenerator] = []
        self.__init_controller()

    def __init_association_tables(self):
        for table in self.metadata.tables.values():
            # Link tables have exactly two foreign key constraints and all columns are involved in them
            # except for special columns like id, inserted, and updated
            fk_constraints = [constr for constr in table.constraints if isinstance(constr, ForeignKeyConstraint)]
            if len(fk_constraints) == 2 and all(
                    col.foreign_keys for col in table.columns if col.name not in self._ignore_columns):
                tablename = sorted(fk_constraints, key=utils.get_constraint_sort_key)[0].elements[0].column.table.name
                self.association_tables[tablename].append(table)

    def render(self, root_directory="."):
        self.__render_objs(self.models, root_directory=root_directory)
        self.__render_objs(self.controllers, root_directory=root_directory)

    def __init_models(self):
        classes = {}
        for table in sorted(self.metadata.tables.values(), key=lambda t: (t.schema or '', t.name)):
            model = ModelGenerator(
                table,
                ignore_cols=self._ignore_columns,
                class_names=self.class_names,
                association_tables=self.association_tables[table.name],
            )
            classes[model.class_name] = model
            self.models.append(model)

        # Resolve any relationships conflicts where one
        # target class might inherit from another
        for model in classes.values():
            visited = []
            for relationship in model.relations.values():
                relationship.make_backref(visited, classes)
                visited.append(relationship)

    def __init_controller(self):
        for model in self.models:
            self.controllers.append(ControllerGenerator(model))

    def __render_objs(self, objs, root_directory="."):
        for obj in objs:
            if self.tables is None:
                if self.ignore_tables and obj.table_name in self.ignore_tables:
                    continue
            else:
                if obj.table_name not in self.tables:
                    continue

            obj.render(root_directory=root_directory)
