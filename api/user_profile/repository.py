"""
    Author: Do Quoc Vuong
    Email: vuongtlt13@gmail.com
    Country: VietNam
    Generated by VGenerator
    Created at: 2021-06-11 17:52:02.906363Z
"""

from api.core import BaseRepository
from api.user_profile.model import UserProfile


class UserProfileRepository(BaseRepository):
    def model(self):
        return UserProfile