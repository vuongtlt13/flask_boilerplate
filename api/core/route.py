import abc

from flask_restx import Resource


class BaseRoute(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = self.get_controller()()

    @abc.abstractmethod
    def get_controller(self):
        raise NotImplemented
