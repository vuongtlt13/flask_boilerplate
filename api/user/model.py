from api.core import BaseModel
from extensions import db


class User(BaseModel):
    __tablename__ = "users"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    username = db.Column(db.String(45), nullable=False, unique=True)
    password = db.Column(db.String(45), nullable=False)
    is_active = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())

    __hidden_columns__ = [
        password
    ]
