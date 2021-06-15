"""
    Author: Do Quoc Vuong
    Email: vuongtlt13@gmail.com
    Country: VietNam
    Generated by VGenerator
    Created at: 2021-06-15 10:23:12.535272Z
"""

from api.core import BaseRepository
from api.application.model import Application


class ApplicationRepository(BaseRepository):
    def model(self):
        return Application
