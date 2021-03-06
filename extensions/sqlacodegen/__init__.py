import codecs
import sys

import click
from flask import Flask
from flask.cli import AppGroup

__all__ = [
    'init_app', 'code_gen'
]

from sqlalchemy import MetaData
# from extensions.sqlacodegen.codegen import CodeGenerator
from extensions.sqlacodegen.code_generator import CodeGenerator


def code_gen(table_name: str, schema=None, class_name=None, no_views=True, no_indexes=False, no_constraints=False,
             no_joined=False, no_classes=None, no_tables=None, outfile=None, no_backrefs=False, ignore_cols=None,
             no_comments=False):
    from extensions import db
    engine = db.engine
    metadata = MetaData(engine)
    metadata.reflect(engine, schema, not no_views, None)
    outfile = codecs.open(outfile, 'w', encoding='utf-8') if outfile else sys.stdout
    generator = CodeGenerator(
        metadata=metadata, no_indexes=no_indexes, no_constraints=no_constraints, no_joined=no_joined,
        ignore_cols=ignore_cols, no_classes=no_classes,
        no_comments=no_comments, no_tables=no_tables, class_name=class_name, table_name=table_name)
    generator.render(outfile)


def init_app(app: Flask):
    codegen_cli = AppGroup('sqlacodegen')

    @codegen_cli.command('generate')
    @click.argument('table_name')
    @click.option('--schema', help='load tables from an alternate schema', default=None)
    @click.option('--class_name', help='name of class Model', default=None)
    @click.option('--outfile', help='file to write output to (default: stdout)', default=None)
    @click.option('--ignore_cols', help="Don't check foreign key constraints on specified columns (comma-separated)",
                  default=None)
    @click.option('--no_views', help="ignore views", default=True)
    @click.option('--no_indexes', help='ignore indexes', default=False)
    @click.option('--no_constraints', help='ignore constraints', default=False)
    @click.option('--no_joined', help="don't autodetect joined table inheritance", default=False)
    @click.option('--no_classes', help="don't generate classes, only tables", default=None)
    @click.option('--no_tables', help="don't generate tables, only classes", default=None)
    @click.option('--no_backrefs', help="don't include backrefs", default=False)
    @click.option('--no_comments', help="don't render column comments", default=False)
    def run(table_name: str, schema=None, class_name=None, no_views=True, no_indexes=False, no_constraints=False,
            no_joined=False, no_classes=None, no_tables=None, outfile=None, no_backrefs=False, ignore_cols=None,
            no_comments=False):
        code_gen(table_name=table_name, schema=schema, class_name=class_name, no_views=no_views, no_indexes=no_indexes,
                 no_constraints=no_constraints, no_joined=no_joined, no_classes=no_classes, no_tables=no_tables,
                 outfile=outfile, no_backrefs=no_backrefs, ignore_cols=ignore_cols, no_comments=no_comments)

    app.cli.add_command(codegen_cli)
