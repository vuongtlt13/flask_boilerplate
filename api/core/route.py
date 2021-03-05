import abc

from flask_restful import Resource


class BaseRoute(Resource):
    def __init__(self):
        self.controller = self.get_controller()()

    @abc.abstractmethod
    def get_controller(self):
        raise NotImplemented
