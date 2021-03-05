import abc
from typing import Dict

from extensions import response


class BaseController:
    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def get(self, id):
        pass

    @abc.abstractmethod
    def create(self, data: Dict):
        pass

    @abc.abstractmethod
    def update(self, id, data: Dict):
        pass

    @abc.abstractmethod
    def delete(self, id):
        pass

    def success(self, message="", data=None):
        return response.success(message=message, data=data)

    def error(self, message="", data=None, error=None):
        return response.error(message=message, data=data, error=error)
