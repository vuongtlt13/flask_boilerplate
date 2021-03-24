from typing import Dict, List
from sqlalchemy import Boolean, ForeignKeyConstraint, Table
from sqlalchemy.util import OrderedDict

from extensions.vgenerator import utils
from extensions.vgenerator.base import BaseGenerator
from extensions.vgenerator.column import ColumnGenerator
from extensions.vgenerator.relationship import ManyToManyRelationship, ManyToOneRelationship, Relationship


class ModelGenerator(BaseGenerator):
    def output_filename(self):
        return "model"

    def __init__(self, table: Table, association_tables: List, class_names: Dict, ignore_cols=None):
        self.class_name = utils.convert_to_class_name((class_names.get(table.name, None)) or table.name)
        super(ModelGenerator, self).__init__(self.class_name)
        self.table = table
        self.table_name = table.name
        self.schema = table.schema
        self.__pre_init()
        self.children = []
        self.ignore_cols = ignore_cols or []
        self.association_tables = association_tables
        self.attributes: Dict[str, ColumnGenerator] = OrderedDict()
        self.relations: Dict[str, Relationship] = OrderedDict()

        # Assign attribute names for columns
        for column in table.columns:
            if column.name in self.ignore_cols:
                continue
            self.attributes[column.name] = ColumnGenerator(column)

        self.__init_relations(class_names)

    def template_file(self):
        return 'extensions/vgenerator/templates/model.mako'

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

    def __init_relations(self, class_names: Dict):
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

    def __pre_init(self):
        # Adapt column types to the most reasonable generic types (ie. VARCHAR -> String)
        for column in self.table.columns:
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
