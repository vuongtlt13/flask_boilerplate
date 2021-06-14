"""
    Author: Do Quoc Vuong
    Email: vuongtlt13@gmail.com
    Country: VietNam
    Generated by VGenerator
    Created at: 2021-06-11 17:52:02.906198Z
"""

from api.core import BaseRepository
from api.option.model import Option


class OptionRepository(BaseRepository):
    def model(self):
        return Option