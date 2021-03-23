from collections import OrderedDict
from typing import Dict

from mako.template import Template
from sqlalchemy import PrimaryKeyConstraint, UniqueConstraint, ForeignKeyConstraint

from extensions.vgenerator import utils


class Relationship(object):
    def __init__(self, source_cls, target_cls):
        super(Relationship, self).__init__()
        self.source_cls = source_cls
        self.target_cls = target_cls
        self.kwargs = OrderedDict()
        self.preferred_name = None
        self.backref_name = utils._underscore(self.source_cls)

    def render(self):
        mytemplate = Template(filename='extensions/vgenerator/templates/relationship.mako')
        return mytemplate.render(**self.get_variables())

    def _render_options(self):
        args = []
        if 'secondaryjoin' in self.kwargs:
            delimiter = ',\n        '
        else:
            delimiter = ', '

        args.extend([key + '=' + value for key, value in self.kwargs.items()])
        return delimiter.join(args)

    def make_backref(self, relationships, classes):
        backref = self.backref_name
        original_backref = backref
        # Check if backref already exists for relationship source_cls to target_cls and add suffix
        suffix = 0
        while (self.target_cls, backref) in [(x.target_cls, x.backref_name) for x in relationships]:
            backref = original_backref + str('_{0}'.format(suffix))
            suffix += 1

        self.kwargs['backref'] = repr(backref)
        # Check if any of the target_cls inherit from other target_cls
        # If so, modify backref name of descendant
        # "backref({0}, lazy='dynamic')".format(repr(backref))
        for rel in [x for x in relationships if 'backref' in x.kwargs]:
            if self.target_cls in classes and rel.target_cls in classes:
                if utils._is_model_descendant(classes[self.target_cls], classes[rel.target_cls]):
                    self.backref_name = self.target_cls.lower() + '_' + backref
                    self.kwargs['backref'] = repr(self.backref_name)
                if utils._is_model_descendant(classes[rel.target_cls], classes[self.target_cls]):
                    backref = rel.backref_name
                    rel.backref_name = rel.target_cls.lower() + '_' + backref
                    rel.kwargs['backref'] = repr(rel.backref_name)

    def get_variables(self) -> Dict:
        return {
            'attribute': self.preferred_name,
            'target_cls': self.target_cls,
            'relation_options': self._render_options()
        }


class ManyToOneRelationship(Relationship):
    def __init__(self, source_cls, target_cls, constraint):
        super(ManyToOneRelationship, self).__init__(source_cls, target_cls)

        column_names = utils.get_column_names_from_constraint(constraint)
        colname = column_names[0]
        tablename = constraint.elements[0].column.table.name
        if not colname.endswith('_id'):
            self.preferred_name = utils.singular_form(tablename) or tablename
        else:
            self.preferred_name = colname[:-3]
        self.backref_name = utils.plural_form(self.backref_name)

        # Add uselist=False to One-to-One relationships
        if any(isinstance(c, (PrimaryKeyConstraint, UniqueConstraint)) and
               set(col.name for col in c.columns) == set(column_names)
               for c in constraint.table.constraints):
            self.kwargs['uselist'] = 'False'

        # Handle self referential relationships
        if source_cls == target_cls:
            self.preferred_name = 'parent' if not colname.endswith('_id') else colname[:-3]
            pk_col_names = [col.name for col in constraint.table.primary_key]
            self.kwargs['remote_side'] = '[{0}]'.format(', '.join(pk_col_names))

        # If the two tables share more than one foreign key constraint,
        # SQLAlchemy needs an explicit primaryjoin to figure out which column(s) to join with
        # common_fk_constraints = _get_common_fk_constraints(constraint.table, constraint.elements[0].column.table)
        # if len(common_fk_constraints) > 1:
        # self.kwargs['primaryjoin'] = "'{0}.{1} == {2}.{3}'".format(source_cls, constraint.columns[0], target_cls, constraint.elements[0].column.name)
        if len(constraint.elements) > 1:  #  or
            self.kwargs['primaryjoin'] = "'and_({0})'".format(', '.join(['{0}.{1} == {2}.{3}'.format(source_cls, k.parent.name, target_cls, k.column.name)
                        for k in constraint.elements]))
        else:
            self.kwargs['primaryjoin'] = "'{0}.{1} == {2}.{3}'".format(source_cls, column_names[0], target_cls,
                                                                       constraint.elements[0].column.name)


class ManyToManyRelationship(Relationship):
    def __init__(self, source_cls, target_cls, association_table):
        super(ManyToManyRelationship, self).__init__(source_cls, target_cls)
        prefix = association_table.schema + '.' if association_table.schema is not None else ''
        self.kwargs['secondary'] = repr(prefix + association_table.name)
        constraints = [c for c in association_table.constraints if isinstance(c, ForeignKeyConstraint)]
        constraints.sort(key=utils.get_constraint_sort_key)
        colname = utils.get_column_names_from_constraint(constraints[1])[0]
        tablename = constraints[1].elements[0].column.table.name
        self.preferred_name = tablename if not colname.endswith('_id') else colname[:-3] + 's'
        self.backref_name = utils.plural_form(self.backref_name)

        # Handle self referential relationships
        if source_cls == target_cls:
            self.preferred_name = 'parents' if not colname.endswith('_id') else colname[:-3] + 's'
            pri_pairs = zip(utils.get_column_names_from_constraint(constraints[0]), constraints[0].elements)
            sec_pairs = zip(utils.get_column_names_from_constraint(constraints[1]), constraints[1].elements)
            pri_joins = ['{0}.{1} == {2}.c.{3}'.format(source_cls, elem.column.name, association_table.name, col)
                         for col, elem in pri_pairs]
            sec_joins = ['{0}.{1} == {2}.c.{3}'.format(target_cls, elem.column.name, association_table.name, col)
                         for col, elem in sec_pairs]
            self.kwargs['primaryjoin'] = (
                repr('and_({0})'.format(', '.join(pri_joins))) if len(pri_joins) > 1 else repr(pri_joins[0]))
            self.kwargs['secondaryjoin'] = (
                repr('and_({0})'.format(', '.join(sec_joins))) if len(sec_joins) > 1 else repr(sec_joins[0]))
