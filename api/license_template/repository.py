"""
    Author: Do Quoc Vuong
    Email: vuongtlt13@gmail.com
    Country: VietNam
    Generated by VGenerator
    Created at: 2021-06-15 10:23:12.536351Z
"""

from api.core import BaseRepository
from api.license_template.model import LicenseTemplate


class LicenseTemplateRepository(BaseRepository):
    def model(self):
        return LicenseTemplate