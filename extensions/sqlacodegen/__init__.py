from typing import Dict, List

import click
from flask import Flask
from flask.cli import AppGroup

__all__ = [
    'init_app', 'code_gen'
]

from sqlalchemy import MetaData
from extensions.sqlacodegen.code_generator import CodeGenerator


def code_gen(tables: List[str] = None, ignore_tables: List[str] = None, schema=None, class_names: Dict = None,
             no_views=True, no_indexes=False, no_constraints=False, no_joined=False, no_classes=None, no_tables=None,
             root_directory: str = ".", ignore_cols=None, no_comments=False):
    from extensions import db
    engine = db.engine
    metadata = MetaData(engine)
    metadata.reflect(engine, schema, not no_views, tables)
    generator = CodeGenerator(
        metadata=metadata, no_indexes=no_indexes, no_constraints=no_constraints, no_joined=no_joined,
        ignore_cols=ignore_cols, no_classes=no_classes, ignore_tables=ignore_tables,
        no_comments=no_comments, no_tables=no_tables, class_names=class_names, tables=tables)
    generator.render(root_directory)


def init_app(app: Flask):
    codegen_cli = AppGroup('vflask')

    @codegen_cli.command('generate')
    @click.option('--tables', help='List tables to processing, use comma to seperate', default=None)
    @click.option('--ignore_tables', help='List tables to ignore, use comma to seperate', default=None)
    @click.option('--schema', help='load tables from an alternate schema', default=None)
    @click.option('--class_names', multiple=True,
                  help='Mapping name between table names and class name, use comma to seperate. Example: \'table_name\',\'class_name\'',
                  default=None)
    @click.option('--root_directory', help='Root directory for generate code (default: ".")', default=".")
    @click.option('--ignore_cols', help="Don't check foreign key constraints on specified columns (comma-separated)",
                  default=None)
    @click.option('--no_views', help="ignore views", default=True)
    @click.option('--no_indexes', help='ignore indexes', default=False)
    @click.option('--no_constraints', help='ignore constraints', default=False)
    @click.option('--no_joined', help="don't autodetect joined table inheritance", default=False)
    @click.option('--no_classes', help="don't generate classes, only tables", default=None)
    @click.option('--no_tables', help="don't generate tables, only classes", default=None)
    @click.option('--no_comments', help="don't render column comments", default=False)
    def run(tables: str = None, ignore_tables: str = None, schema=None, class_names: str = None,
            no_views=True, root_directory: str = ".", no_indexes=False, no_constraints=False, no_joined=False,
            no_classes=None, no_tables=None, ignore_cols=None, no_comments=False):

        tables = tables.split(",") if tables else None
        ignore_tables = ignore_tables.split(",") if ignore_tables else None

        class_names = {x.split(",")[0]: x.split(",")[1] for x in class_names}
        code_gen(tables=tables, ignore_tables=ignore_tables, schema=schema, class_names=class_names, no_views=no_views,
                 no_indexes=no_indexes, no_constraints=no_constraints, no_joined=no_joined, no_classes=no_classes,
                 no_tables=no_tables, root_directory=root_directory, ignore_cols=ignore_cols, no_comments=no_comments)

    app.cli.add_command(codegen_cli)
