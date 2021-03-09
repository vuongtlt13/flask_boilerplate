import inspect
import sys
from keyword import iskeyword
from typing import List
import inflect
import re

from sqlalchemy import CheckConstraint, ForeignKeyConstraint, Enum, UniqueConstraint, ForeignKey
from sqlalchemy.sql.elements import TextClause

_re_boolean_check_constraint = re.compile(r"(?:(?:.*?)\.)?(.*?) IN \(0, 1\)")
_re_column_name = re.compile(r'(?:(["`]?)(?:.*)\1\.)?(["`]?)(.*)\2')
_re_enum_check_constraint = re.compile(r"(?:(?:.*?)\.)?(.*?) IN \((.+)\)")
_re_enum_item = re.compile(r"'(.*?)(?<!\\)'")
_re_invalid_identifier = re.compile(r'[^a-zA-Z0-9_]' if sys.version_info[0] < 3 else r'(?u)\W')

_re_first_cap = re.compile('(.)([A-Z][a-z]+)')
_re_all_cap = re.compile('([a-z0-9])([A-Z])')

_flask_prepend = 'db.'

inflect_engine = inflect.engine()


def get_timestamps_columns() -> List[str]:
    return [
        "created_at",
        "updated_at"
    ]


class _DummyInflectEngine(object):
    def singular_noun(self, noun):
        return noun
    def plural_noun(self, noun):  # needed for backrefs
        import inflect
        inflect_engine = inflect.engine()
        return inflect_engine.plural_noun(noun)


def _convert_to_valid_identifier(name):
    assert name, 'Identifier cannot be empty'
    if name[0].isdigit() or iskeyword(name):
        name = '_' + name
    return _re_invalid_identifier.sub('_', name)


def _get_common_fk_constraints(table1, table2):
    """Returns a set of foreign key constraints the two tables have against each other."""
    c1 = set(c for c in table1.constraints if isinstance(c, ForeignKeyConstraint) and
             c.elements[0].column.table == table2)
    c2 = set(c for c in table2.constraints if isinstance(c, ForeignKeyConstraint) and
             c.elements[0].column.table == table1)
    return c1.union(c2)


def _underscore(name):
    """Converts CamelCase to camel_case. See http://stackoverflow.com/questions/1175208"""
    s1 = _re_first_cap.sub(r'\1_\2', name)
    return _re_all_cap.sub(r'\1_\2', s1).lower()


def _is_model_descendant(model_a, model_b):
    """Check to see if model class A inherits from another model class B"""
    if model_a.class_name == model_b.class_name:
        return True
    if not model_b.children:
        return False
    return any(_is_model_descendant(model_a, b) for b in model_b.children)


def _render_index(index):
    columns = [repr(col.name) for col in index.columns]
    return _flask_prepend + 'Index({0!r}, {1})'.format(index.name, ', '.join(columns))


def pascal_case(words: str) -> str:
    return words.lower().replace("_", " ").title().replace(" ", "")


def singular_form(word: str) -> str:
    singular = inflect_engine.singular_noun(word)
    if isinstance(singular, bool):
        return word
    return singular


def convert_to_class_name(snake_case_words: str) -> str:
    return pascal_case(singular_form(snake_case_words))


def get_column_names_from_constraint(constraint):
    if isinstance(constraint.columns, list):
        return constraint.columns
    return list(constraint.columns.keys())


def plural_form(word: str) -> str:
    plural = inflect_engine.plural_noun(word)
    if isinstance(plural, bool):
        return word
    return plural


def get_constraint_sort_key(constraint):
    if isinstance(constraint, CheckConstraint):
        return 'C{0}'.format(constraint.sqltext)
    return constraint.__class__.__name__[0] + repr(get_column_names_from_constraint(constraint))
