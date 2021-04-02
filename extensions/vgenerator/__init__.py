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
             root_directory: str = ".", ignore_cols=None, no_comments=False, auth_tables=None,
             password_columns=None):
    from extensions import db
    engine = db.engine
    metadata = MetaData(engine)
    metadata.reflect(engine, schema, False, tables)
    generator = CodeGenerator(
        metadata=metadata, ignore_cols=ignore_cols, ignore_tables=ignore_tables, no_comments=no_comments,
        class_names=class_names, tables=tables, auth_tables=auth_tables, password_columns=password_columns)
    generator.render(root_directory)


def init_app(app: Flask):
    codegen_cli = AppGroup('vgenerator')

    @codegen_cli.command('generate')
    @click.option('--tables', help='List tables to processing, use comma to separate', default=None)
    @click.option('--ignore-tables', help='List tables to ignore, use comma to separate', default=None)
    @click.option('--schema', help='load tables from an alternate schema', default=None)
    @click.option('--class-names', multiple=True,
                  help='Mapping name between table names and class name, use comma to '
                       'separate (\'table_name\',\'class_name\') and could use many times. Example: users,User',
                  default=None)
    @click.option('--root-directory', help='Root directory for generate code (default: ".")', default=".")
    @click.option('--auth-tables', help='Authenticate tables, use comma to separate. Default: users,user', default="users,user")
    @click.option('--password-columns', help='Password columns for hashing, use comma to separate. Default: password', default="password")
    @click.option('--ignore-cols', help="Don't check foreign key constraints on specified columns (comma-separated)",
                  default=None)
    @click.option('--no_comments', help="don't render column comments", default=False)
    def run(tables: str = None, ignore_tables: str = None, schema=None, class_names: str = None,
            root_directory: str = ".", auth_tables="users,user", password_columns="password", ignore_cols=None,
            no_comments=False):

        tables = tables.split(",") if tables else None
        ignore_tables = ignore_tables.split(",") if ignore_tables else None
        auth_tables = auth_tables.split(",") if auth_tables else None
        password_columns = password_columns.split(",") if password_columns else None

        class_names = {x.split(",")[0]: x.split(",")[1] for x in class_names}
        code_gen(tables=tables, ignore_tables=ignore_tables, schema=schema, class_names=class_names,
                 root_directory=root_directory, ignore_cols=ignore_cols, no_comments=no_comments,
                 auth_tables=auth_tables, password_columns=password_columns)

    app.cli.add_command(codegen_cli)
