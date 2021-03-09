from api.core import BaseModel
from extensions import db


class Company(BaseModel):
    __tablename__ = "companies"
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(45), nullable=False, unique=True)
