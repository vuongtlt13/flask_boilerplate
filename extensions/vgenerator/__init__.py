import copy
from typing import Dict, List, Optional

import click
from flask import Flask
from flask.cli import AppGroup

__all__ = [
    'VGenerator'
]

from sqlalchemy import MetaData, create_engine
from sqlalchemy.engine import Engine

from extensions.vgenerator.main import CodeGenerator


class VGenerator(object):
    def __init__(self, app: Flask = None):
        self.app = None
        self.design_uri = None
        self.engine: Optional[Engine] = None
        self.database_name = None
        self.metadata = None
        if app:
            self.init_app(app)

    def code_gen(self, tables: List[str] = None, ignore_tables: List[str] = None, schema=None, class_names: Dict = None,
                 root_directory: str = ".", ignore_cols=None, no_comments=False, auth_tables=None,
                 password_columns=None, skips=None):

        if skips is None:
            skips = []

        self.metadata.reflect(self.engine, schema, False, tables)
        generator = CodeGenerator(
            metadata=self.metadata, ignore_cols=ignore_cols, ignore_tables=ignore_tables, no_comments=no_comments,
            class_names=class_names, tables=tables, auth_tables=auth_tables, password_columns=password_columns, skips=skips)
        generator.render(root_directory)

    def init_app(self, app: Flask):
        self.app = app
        self.database_name = self.app.config.get('DESIGN_SQLALCHEMY_DBNAME')
        self.design_uri = app.config.get('DESIGN_SQLALCHEMY_DATABASE_URI')
        self.engine = self.get_engine()
        self.metadata = MetaData(self.engine)

        if not self.is_database_exists():
            self.create_database()

        self.init_commands()

    def get_engine(self) -> Engine:
        engine = create_engine(self.design_uri)
        return engine

    def is_database_exists(self):
        try:
            conn = self.engine.connect()
            print("Database exists!")
            return True
        except Exception as e:
            print(f"Database does not exist!")
            return False

    def create_database(self):
        try:
            connection_url = f'{self.engine.url.drivername}' \
                             f'://{self.engine.url.username}:{self.engine.url.password}' \
                             f'@{self.engine.url.host}:{self.engine.url.port}'
            engine = create_engine(connection_url)
            conn = engine.connect()
            conn.execute("commit")
            conn.execute(f"create database {self.database_name};")
            conn.close()
            print("Create design database successfully!")
        except Exception as e:
            raise

    def init_commands(self):
        codegen_cli = AppGroup('vgenerator')
        metadata = self.metadata
        main_app = self.app

        @codegen_cli.command('generate')
        @click.option('--tables', help='List tables to processing, use comma to separate', default=None)
        @click.option('--ignore-tables', help='List tables to ignore, use comma to separate', default=None)
        @click.option('--schema', help='load tables from an alternate schema', default=None)
        @click.option('--class-names', multiple=True,
                      help='Mapping name between table names and class name, use comma to '
                           'separate (\'table_name\',\'class_name\') and could use many times. Example: users,User',
                      default=None)
        @click.option('--skips', help='Skip generating modules, must in (model, controller, repository, schema, route). Use comma to separate', default="api")
        @click.option('--root-directory', help='Root directory for generate code (default: "api")', default="api")
        @click.option('--auth-tables', help='Authenticate tables, use comma to separate. Default: users,user',
                      default="users,user")
        @click.option('--password-columns',
                      help='Password columns for hashing, use comma to separate. Default: password', default="password")
        @click.option('--ignore-cols',
                      help="Don't check foreign key constraints on specified columns (comma-separated)",
                      default=None)
        @click.option('--no_comments', help="don't render column comments", default=False)
        def generate(tables: str = None, ignore_tables: str = None, schema=None, class_names: str = None,
                     root_directory: str = "api", auth_tables="users,user", password_columns="password", ignore_cols=None,
                     no_comments=False, skips=None):
            tables = tables.split(",") if tables else None
            skips = skips.split(",") if skips else []
            ignore_tables = ignore_tables.split(",") if ignore_tables else None
            auth_tables = auth_tables.split(",") if auth_tables else None
            password_columns = password_columns.split(",") if password_columns else None

            class_names = {x.split(",")[0]: x.split(",")[1] for x in class_names}
            self.code_gen(tables=tables, ignore_tables=ignore_tables, schema=schema, class_names=class_names,
                          root_directory=root_directory, ignore_cols=ignore_cols, no_comments=no_comments,
                          auth_tables=auth_tables, password_columns=password_columns, skips=skips)

        @codegen_cli.command('sync')
        def sync_tables():
            app = Flask(__name__)
            config = copy.deepcopy(main_app.config)
            config['SQLALCHEMY_DATABASE_URI'] = config['DESIGN_SQLALCHEMY_DATABASE_URI']
            config['DATABASE_URI'] = config['DESIGN_SQLALCHEMY_DATABASE_URI']
            app.config = config
            from flask_sqlalchemy import SQLAlchemy
            db = SQLAlchemy()
            db.init_app(app=app)
            db.Model = main_app.extensions['sqlalchemy'].db.Model
            metadata.reflect()
            metadata.drop_all()
            db.create_all(app=app)

        self.app.cli.add_command(codegen_cli)
