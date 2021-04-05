import abc
from typing import Dict

from extensions import response


class BaseController:
    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def get(self, _id):
        pass

    @abc.abstractmethod
    def create(self, data: Dict):
        pass

    @abc.abstractmethod
    def update(self, _id, data: Dict):
        pass

    @abc.abstractmethod
    def delete(self, _id):
        pass

    def success(self, data=None):
        return response.success(data=data)

    def error(self, data=None, error=None):
        return response.error(data=data, error=error)
