import sys
from collections import defaultdict

from mako.template import Template
from sqlalchemy import ForeignKeyConstraint

from extensions.sqlacodegen import utils
from extensions.sqlacodegen.model_generator import ModelGenerator


class CodeGenerator(object):
    def __init__(self, metadata, table_name: str, class_name: str = None,
                 ignore_cols=None,
                 no_indexes: bool = False,
                 no_constraints: bool = False,
                 no_joined: bool = False,
                 no_classes=False,
                 no_comments=False,
                 no_tables=False
                 ):
        """
        :param metadata:
        :param table_name:
        :param class_name:
        :param no_indexes:
        :param no_constraints:
        :param no_joined:
        :param ignore_cols:
        :param no_classes:
        :param no_comments:
        :param no_tables:
        """
        super(CodeGenerator, self).__init__()

        # exclude these column names from consideration when generating association tables
        self.metadata = metadata
        self._ignore_columns = ignore_cols or [] + utils.get_timestamps_columns()

        self.no_comments = no_comments

        self.association_tables = defaultdict(lambda: [])
        self._init_association_tables()
        # Iterate through the tables and create model classes when possible
        self.models = []
        self.table_name = table_name
        classes = {}
        for table in sorted(metadata.tables.values(), key=lambda t: (t.schema or '', t.name)):
            # Support for Alembic and sqlalchemy-migrate -- never expose the schema version tables
            dest_class_name = None
            if table.name == table_name:
                dest_class_name = class_name
            model = ModelGenerator(
                table,
                class_name=dest_class_name,
                ignore_cols=self._ignore_columns,
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

    def render(self, outfile=sys.stdout):
        # Render the collected imports
        res_model = None
        for model in self.models:
            if model.table.name == self.table_name:
                res_model = model
                break
        model_variables = res_model.get_variables()
        mytemplate = Template(filename='extensions/sqlacodegen/templates/model.mako')
        print(mytemplate.render(**model_variables).rstrip("\n"), file=outfile)
