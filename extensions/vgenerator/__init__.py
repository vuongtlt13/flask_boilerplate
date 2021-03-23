from typing import Dict, List

import click
from flask import Flask
from flask.cli import AppGroup

__all__ = [
    'init_app', 'code_gen'
]

from sqlalchemy import MetaData
from extensions.vgenerator.main import CodeGenerator


def code_gen(tables: List[str] = None, ignore_tables: List[str] = None, schema=None, class_names: Dict = None,
             root_directory: str = ".", ignore_cols=None, no_comments=False):
    from extensions import db
    engine = db.engine
    metadata = MetaData(engine)
    metadata.reflect(engine, schema, False, tables)
    generator = CodeGenerator(
        metadata=metadata, ignore_cols=ignore_cols, ignore_tables=ignore_tables, no_comments=no_comments,
        class_names=class_names, tables=tables)
    generator.render(root_directory)


def init_app(app: Flask):
    codegen_cli = AppGroup('vgenerator')

    @codegen_cli.command('generate')
    @click.option('--tables', help='List tables to processing, use comma to seperate', default=None)
    @click.option('--ignore_tables', help='List tables to ignore, use comma to seperate', default=None)
    @click.option('--schema', help='load tables from an alternate schema', default=None)
    @click.option('--class_names', multiple=True,
                  help='Mapping name between table names and class name, use comma to seperate (\'table_name\',\'class_name\') and could use many times. Example: users,User',
                  default=None)
    @click.option('--root_directory', help='Root directory for generate code (default: ".")', default=".")
    @click.option('--ignore_cols', help="Don't check foreign key constraints on specified columns (comma-separated)",
                  default=None)
    @click.option('--no_comments', help="don't render column comments", default=False)
    def run(tables: str = None, ignore_tables: str = None, schema=None, class_names: str = None,
            root_directory: str = ".", ignore_cols=None, no_comments=False):

        tables = tables.split(",") if tables else None
        ignore_tables = ignore_tables.split(",") if ignore_tables else None

        class_names = {x.split(",")[0]: x.split(",")[1] for x in class_names}
        code_gen(tables=tables, ignore_tables=ignore_tables, schema=schema, class_names=class_names,
                 root_directory=root_directory, ignore_cols=ignore_cols, no_comments=no_comments)

    app.cli.add_command(codegen_cli)
