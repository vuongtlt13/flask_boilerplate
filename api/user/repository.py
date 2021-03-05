from api.core import BaseRepository
from api.user.model import User


class UserRepository(BaseRepository):
    def model(self):
        return User
