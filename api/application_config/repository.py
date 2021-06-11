"""
    Author: Do Quoc Vuong
    Email: vuongtlt13@gmail.com
    Country: VietNam
    Generated by VGenerator
    Created at: 2021-06-11 17:52:02.904495Z
"""

from api.core import BaseRepository
from api.application_config.model import ApplicationConfig


class ApplicationConfigRepository(BaseRepository):
    def model(self):
        return ApplicationConfig
