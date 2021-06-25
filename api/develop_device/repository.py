"""
    Author: Do Quoc Vuong
    Email: vuongtlt13@gmail.com
    Country: VietNam
    Generated by VGenerator
    Created at: 2021-06-15 10:23:12.535505Z
"""

from api.core import BaseRepository
from api.develop_device.model import DevelopDevice


class DevelopDeviceRepository(BaseRepository):
    def model(self):
        return DevelopDevice