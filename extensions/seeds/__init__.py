import glob
import os
import click
import sqlalchemy as sa
from alembic.operations import Operations
from alembic.runtime.migration import MigrationContext
from flask import Flask
from flask.cli import AppGroup
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, column, table

seed_table = table('seeds',
                   column('file', String),
                   )


def init_online(app: Flask):
    db: SQLAlchemy = app.extensions['sqlalchemy'].db
    conn = db.engine.connect()
    ctx = MigrationContext.configure(conn)
    op = Operations(ctx)
    try:
        op.drop_table('seeds')
    except:
        pass
    op.create_table('seeds', sa.Column('file', sa.String(255), primary_key=True))


def fetch_all_run_seeds(app: Flask):
    db: SQLAlchemy = app.extensions['sqlalchemy'].db
    conn = db.engine.connect()
    res = conn.execute("select * from seeds")
    results = res.fetchall()
    run_seeds = [{'file': r[0]} for r in results]
    return [run_seed['file'] for run_seed in run_seeds]


def execute_script(app, seed_file: str):
    file_name = os.path.basename(seed_file)
    file_name_without_extension = file_name.replace(".py", "")
    working_directory = os.path.abspath(os.getcwd())
    relative_path = os.path.relpath(os.path.dirname(seed_file), working_directory)
    module_path = relative_path.replace("/", ".").replace("\\", ".")

    db: SQLAlchemy = app.extensions['sqlalchemy'].db
    exec(f"from {module_path}.{file_name_without_extension} import run")
    eval(f"run(db)")
    conn = db.engine.connect()
    ctx = MigrationContext.configure(conn)
    op = Operations(ctx)
    op.bulk_insert(seed_table,
        [
            {'file': file_name_without_extension},
        ]
    )


def init_app(app: Flask):
    seed_cli = AppGroup('seed')

    @seed_cli.command('init')
    def init():
        init_online(app)

    @seed_cli.command('new')
    def new():
        action_name = input("Action name: ")
        if not action_name:
            action_name = ""
        if action_name == "" or "." in action_name or len(action_name) > 125:
            print("File name is invalid!")
            return
        directory = os.path.dirname(os.path.abspath(__file__))
        filename = f'{action_name}.py'
        file_path = os.path.join(directory, filename)
        try:
            seed_file = open(file_path, "w+")
            seed_file.write("def run():\n")
            seed_file.write("   # Seeding here\n")
            seed_file.write("   pass\n")
            seed_file.close()
        except Exception as e:
            os.unlink(file_path)
            print("Can't create file")
            print(str(e))

    @seed_cli.command('run')
    @click.option('--path', multiple=True,
                  help='Path file to execute seeding',
                  default=None)
    def run(path=None):
        run_seeds = fetch_all_run_seeds(app)
        directory = os.path.dirname(os.path.abspath(__file__))
        for seed_file in glob.glob(os.path.join(directory, '*.py')):
            file_name = os.path.basename(seed_file)
            file_name_without_extension = file_name.replace(".py", "")
            if file_name_without_extension == "__init__" or file_name_without_extension in run_seeds:
                continue
            if (path and file_name == path or file_name_without_extension == path) or not path:
                execute_script(app, seed_file)

    app.cli.add_command(seed_cli)
