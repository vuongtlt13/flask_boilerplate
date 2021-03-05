from api.core import BaseModel
from extensions import db


class User(BaseModel):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    username = db.Column(db.String(45), nullable=False, unique=True)
    password = db.Column(db.String(45), nullable=False)

    __hidden_columns__ = [
        password
    ]
