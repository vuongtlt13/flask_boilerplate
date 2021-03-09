import os
import sys
from collections import defaultdict
from typing import Dict, List

from mako.template import Template
from sqlalchemy import ForeignKeyConstraint

from extensions.sqlacodegen import utils
from extensions.sqlacodegen.model_generator import ModelGenerator


class CodeGenerator(object):
    def __init__(self, metadata,
                 tables: List[str] = None,
                 ignore_tables: List[str] = None,
                 class_names: Dict = None,
                 ignore_cols=None,
                 no_indexes: bool = False,
                 no_constraints: bool = False,
                 no_joined: bool = False,
                 no_classes=False,
                 no_comments=False,
                 no_tables=False
                 ):
        """

        Args:
            metadata:
            tables:
            ignore_tables:
            class_names:
            ignore_cols:
            no_indexes:
            no_constraints:
            no_joined:
            no_classes:
            no_comments:
            no_tables:
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
        self._init_association_tables()
        # Iterate through the tables and create model classes when possible
        self.models = []
        classes = {}
        for table in sorted(metadata.tables.values(), key=lambda t: (t.schema or '', t.name)):
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

    def _init_association_tables(self):
        for table in self.metadata.tables.values():
            # Link tables have exactly two foreign key constraints and all columns are involved in them
            # except for special columns like id, inserted, and updated
            fk_constraints = [constr for constr in table.constraints if isinstance(constr, ForeignKeyConstraint)]
            if len(fk_constraints) == 2 and all(
                    col.foreign_keys for col in table.columns if col.name not in self._ignore_columns):
                tablename = sorted(fk_constraints, key=utils.get_constraint_sort_key)[0].elements[0].column.table.name
                self.association_tables[tablename].append(table)

    def render(self, root_directory="."):
        for model in self.models:
            if self.tables is None:
                if self.ignore_tables and model.table.name in self.ignore_tables:
                    continue
            else:
                if model.table.name not in self.tables:
                    continue

            outfile = self.get_outfile(root_directory=root_directory, class_name=model.class_name)
            model_variables = model.get_variables()
            mytemplate = Template(filename='extensions/sqlacodegen/templates/model.mako')
            res = mytemplate.render(**model_variables).rstrip("\n")
            print(res)
            print(res, file=outfile)
            outfile.close()

    def get_outfile(self, root_directory: str, class_name: str):
        directory = f'{root_directory}/{class_name.lower()}'
        file_path = f"{directory}/model.py"
        if not os.path.exists(directory):
            os.mkdir(directory)
        return open(file_path, 'w+', encoding='utf8')
