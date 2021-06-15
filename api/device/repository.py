"""
    Author: Do Quoc Vuong
    Email: vuongtlt13@gmail.com
    Country: VietNam
    Generated by VGenerator
    Created at: 2021-06-15 10:23:12.535716Z
"""

from api.core import BaseRepository
from api.device.model import Device


class DeviceRepository(BaseRepository):
    def model(self):
        return Device
