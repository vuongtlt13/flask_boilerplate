import inspect

from mako.template import Template
from sqlalchemy import Column, UniqueConstraint, ForeignKey, ForeignKeyConstraint, CheckConstraint
from sqlalchemy.sql.elements import TextClause

from extensions.sqlacodegen import utils


class ColumnGenerator(object):
    def __init__(self, column: Column):
        self.column = column

    def render(self):
        mytemplate = Template(filename='extensions/sqlacodegen/templates/attribute.mako')
        return mytemplate.render(**self.get_variables())

    def get_variables(self):
        return {
            "column_name": self.column.name,
            "column_type": self._render_column_type(),
            "column_options": self._render_options()
        }

    def _render_column_type(self):
        args = []
        # All other types
        argspec = self._getargspec_init()
        defaults = dict(zip(argspec.args[-len(argspec.defaults or ()):], argspec.defaults or ()))
        missing = object()
        use_kwargs = False
        for attr in argspec.args[1:]:
            # Remove annoyances like _warn_on_bytestring
            if attr.startswith('_'):
                continue

            value = getattr(self.column.type, attr, missing)
            default = defaults.get(attr, missing)
            if value is missing or value == default:
                use_kwargs = True
            elif use_kwargs:
                args.append('{0}={1}'.format(attr, repr(value)))
            else:
                args.append(repr(value))

        text = self.column.type.__class__.__name__

        if args:
            text += '({0})'.format(', '.join(args))

        return text

    def _get_compiled_expression(self, statement):
        """Returns the statement in a form where any placeholders have been filled in."""
        if isinstance(statement, TextClause):
            return statement.text

        dialect = statement._from_objects[0].bind.dialect
        compiler = statement._compiler(dialect)

        # Adapted from http://stackoverflow.com/a/5698357/242021
        class LiteralCompiler(compiler.__class__):
            def visit_bindparam(self, bindparam, within_columns_clause=False, literal_binds=False, **kwargs):
                return super(LiteralCompiler, self).render_literal_bindparam(
                    bindparam, within_columns_clause=within_columns_clause,
                    literal_binds=literal_binds, **kwargs
                )

        compiler = LiteralCompiler(dialect, statement)
        return compiler.process(statement)

    def _render_constraint(self, constraint):
        def render_fk_options(*opts):
            opts = [repr(opt) for opt in opts]
            for attr in 'ondelete', 'onupdate', 'deferrable', 'initially', 'match':
                value = getattr(constraint, attr, None)
                if value:
                    opts.append('{0}={1!r}'.format(attr, value))

            return ', '.join(opts)

        if isinstance(constraint, ForeignKey):
            remote_column = '{0}.{1}'.format(constraint.column.table.fullname, constraint.column.name)
            return 'db.ForeignKey({0})'.format(render_fk_options(remote_column))
        elif isinstance(constraint, ForeignKeyConstraint):
            local_columns = utils.get_column_names_from_constraint(constraint)
            remote_columns = ['{0}.{1}'.format(fk.column.table.fullname, fk.column.name)
                              for fk in constraint.elements]
            return 'db.ForeignKeyConstraint({0})'.format(render_fk_options(local_columns, remote_columns))
        elif isinstance(constraint, CheckConstraint):
            return 'db.CheckConstraint({0!r})'.format(self._get_compiled_expression(constraint.sqltext))
        elif isinstance(constraint, UniqueConstraint):
            columns = [repr(col.name) for col in constraint.columns]
            return 'db.UniqueConstraint({0})'.format(', '.join(columns))

    def _getargspec_init(self):
        method = self.column.type.__class__.__init__
        try:
            return inspect.getargspec(method)
        except TypeError:
            if method is object.__init__:
                return inspect.ArgSpec(['self'], None, None, None)
            else:
                return inspect.ArgSpec(['self'], 'args', 'kwargs', None)

    def _render_options(self):
        kwarg = []
        is_sole_pk = self.column.primary_key and len(self.column.table.primary_key) == 1
        dedicated_fks = [c for c in self.column.foreign_keys if len(c.constraint.columns) == 1]
        is_unique = any(isinstance(c, UniqueConstraint) and set(c.columns) == {self.column}
                        for c in self.column.table.constraints)
        is_unique = is_unique or any(i.unique and set(i.columns) == {self.column} for i in self.column.table.indexes)
        has_index = any(set(i.columns) == {self.column} for i in self.column.table.indexes)

        if self.column.key != self.column.name:
            kwarg.append('key')
        if self.column.primary_key:
            kwarg.append('primary_key')
        if not self.column.nullable and not is_sole_pk:
            kwarg.append('nullable')
        if is_unique:
            self.column.unique = True
            kwarg.append('unique')
        elif has_index:
            self.column.index = True
            kwarg.append('index')
        if self.column.server_default:
            server_default = 'server_default=db.FetchedValue()'

        comment = getattr(self.column, 'comment', None)
        return ', '.join(
            [self._render_constraint(x) for x in dedicated_fks] +
            [repr(x) for x in self.column.constraints] +
            ['{0}={1}'.format(k, repr(getattr(self.column, k))) for k in kwarg] +
            ([server_default] if self.column.server_default else []) +
            (['info={!r}'.format(comment)] if comment else [])
        )
