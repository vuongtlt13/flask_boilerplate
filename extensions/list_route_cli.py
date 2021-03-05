from flask import Flask
from flask.cli import AppGroup


def init_app(app: Flask):
    route_cli = AppGroup('route')

    @route_cli.command('list')
    def list_routes():
        for rule in app.url_map.iter_rules():
            print(f"{str(rule.rule):<50s}{str(rule.methods):50s}{str(rule.endpoint)}")

    app.cli.add_command(route_cli)
