from typing import Dict, List

from sqlalchemy import Boolean, ForeignKeyConstraint, Table
from sqlalchemy.util import OrderedDict

from extensions.sqlacodegen import utils
from extensions.sqlacodegen.column_generator import ColumnGenerator
from extensions.sqlacodegen.relationship import ManyToManyRelationship, ManyToOneRelationship


class Model(object):
    def __init__(self, table: Table):
        super(Model, self).__init__()
        self.table = table
        self.schema = table.schema

        # Adapt column types to the most reasonable generic types (ie. VARCHAR -> String)
        for column in table.columns:
            cls = column.type.__class__
            if cls.__name__ == 'TINYINT' and column.type.display_width == 1:
                cls = Boolean
            else:
                for supercls in cls.__mro__:
                    if hasattr(supercls, '__visit_name__'):
                        cls = supercls
                    if supercls.__name__ != supercls.__name__.upper() and not supercls.__name__.startswith('_'):
                        break

            column.type = column.type.adapt(cls)


class ModelGenerator(Model):
    parent_name = 'Base'

    def __init__(self, table: Table, association_tables: List, class_names: Dict, ignore_cols=None):
        super(ModelGenerator, self).__init__(table)
        self.class_name = (class_names.get(table.name, None)) or utils.convert_to_class_name(table.name)
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

        self._init_relations(class_names)

    def get_variables(self) -> Dict:
        return {
            "class_name": self.class_name,
            "table_name": self.table.name,
            "columns": self.render_columns(),
            "hidden_columns": self.render_hidden_columns(),
            "relationships": self.render_relationships()
        }

    def render_columns(self) -> List[str]:
        # Render columns
        res = []
        for attr, column in self.attributes.items():
            res.append(column.render())
        return res

    def render_hidden_columns(self) -> List[str]:
        return []

    def render_relationships(self) -> List[str]:
        res = []
        # Render relationships
        for attr, relationship in self.relations.items():
            res.append(relationship.render())
        return res

    def _init_relations(self, class_names: Dict):
        # Add many-to-one relationships
        for constraint in sorted(self.table.constraints, key=utils.get_constraint_sort_key):
            if isinstance(constraint, ForeignKeyConstraint):
                source_cls = class_names.get(self.table.name, None) or utils.convert_to_class_name(self.table.name)
                target_cls = class_names.get(constraint.elements[0].column.table.name, None) or utils.convert_to_class_name(constraint.elements[0].column.table.name)
                relationship_ = ManyToOneRelationship(source_cls, target_cls, constraint)
                self.relations[relationship_.preferred_name] = relationship_

        # Add many-to-many relationships
        for association_table in self.association_tables:
            fk_constraints = [c for c in association_table.constraints if isinstance(c, ForeignKeyConstraint)]
            fk_constraints.sort(key=utils.get_constraint_sort_key)
            source_cls = class_names.get(self.table.name, None) or utils.convert_to_class_name(self.table.name)
            target_cls = class_names.get(fk_constraints[1].elements[0].column.table.name, None) or utils.convert_to_class_name(
                fk_constraints[1].elements[0].column.table.name)
            relationship_ = ManyToManyRelationship(source_cls, target_cls, association_table)
            self.relations[relationship_.preferred_name] = relationship_
