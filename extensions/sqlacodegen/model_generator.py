from typing import Dict, Optional, List

from sqlalchemy import Table, PrimaryKeyConstraint, ForeignKeyConstraint, UniqueConstraint, Column
from sqlalchemy.util import OrderedDict

from extensions.sqlacodegen import utils
from extensions.sqlacodegen.codegen import Relationship
from extensions.sqlacodegen.column_generator import ColumnGenerator
from extensions.sqlacodegen.relationship import ManyToOneRelationship, ManyToManyRelationship


class Model(object):
    def __init__(self, table):
        super(Model, self).__init__()
        self.table = table
        self.schema = table.schema

        # Adapt column types to the most reasonable generic types (ie. VARCHAR -> String)
        for column in table.columns:
            cls = column.type.__class__
            for supercls in cls.__mro__:
                if hasattr(supercls, '__visit_name__'):
                    cls = supercls
                if supercls.__name__ != supercls.__name__.upper() and not supercls.__name__.startswith('_'):
                    break

            column.type = column.type.adapt(cls)

    def add_imports(self, collector):
        if self.table.columns:
            collector.add_import(Column)

        for column in self.table.columns:
            collector.add_import(column.type)
            if column.server_default:
                collector.add_literal_import('sqlalchemy.schema', 'FetchedValue')

        for constraint in sorted(self.table.constraints, key=utils.get_constraint_sort_key):
            if isinstance(constraint, ForeignKeyConstraint):
                if len(constraint.columns) > 1:
                    collector.add_literal_import('sqlalchemy', 'ForeignKeyConstraint')
                else:
                    collector.add_literal_import('sqlalchemy', 'ForeignKey')
            elif isinstance(constraint, UniqueConstraint):
                if len(constraint.columns) > 1:
                    collector.add_literal_import('sqlalchemy', 'UniqueConstraint')
            elif not isinstance(constraint, PrimaryKeyConstraint):
                collector.add_import(constraint)

        for index in self.table.indexes:
            if len(index.columns) > 1:
                collector.add_import(index)


class ModelGenerator(Model):
    parent_name = 'Base'

    def __init__(self, table: Table, association_tables: List, class_name: str = None, ignore_cols=None):
        super(ModelGenerator, self).__init__(table)
        self.class_name = class_name or utils.convert_to_class_name(table.name)
        self.children = []
        self.ignore_cols = ignore_cols or []
        self.association_tables = association_tables
        self.attributes = OrderedDict()
        self.relations = OrderedDict()

        # Assign attribute names for columns
        for column in table.columns:
            if column.name in self.ignore_cols:
                continue
            self.attributes[column.name] = ColumnGenerator(column)

        self._init_relations()

    def get_variables(self) -> Dict:
        return {
            "class_name": self.class_name,
            "table_name": self.table.name,
            "columns": self.render_columns(),
            "hidden_columns": self.render_hidden_columns(),
            "relationships": self.render_relationships()
        }

    def render_columns(self) -> str:
        # Render columns
        res = '\n'
        for attr, column in self.attributes.items():
            res += column.render()
        return res

    def render_hidden_columns(self) -> Optional[str]:
        return None

    def render_relationships(self) -> str:
        res = ''
        # Render relationships
        for attr, relationship in self.relations.items():
            res += '{0} = {1}\n'.format(attr, relationship.render())
        return res

    def _init_relations(self):
        # Add many-to-one relationships
        for constraint in sorted(self.table.constraints, key=utils.get_constraint_sort_key):
            if isinstance(constraint, ForeignKeyConstraint):
                target_cls = utils.convert_to_class_name(constraint.elements[0].column.table.name)
                relationship_ = ManyToOneRelationship(self.table.name, target_cls, constraint)
                self.relations[relationship_.preferred_name] = relationship_

        # Add many-to-many relationships
        for association_table in self.association_tables:
            fk_constraints = [c for c in association_table.constraints if isinstance(c, ForeignKeyConstraint)]
            fk_constraints.sort(key=utils.get_constraint_sort_key)
            target_cls = utils.convert_to_class_name(fk_constraints[1].elements[0].column.table.name)
            relationship_ = ManyToManyRelationship(self.table.name, target_cls, association_table)
            self.relations[relationship_.preferred_name] = relationship_
