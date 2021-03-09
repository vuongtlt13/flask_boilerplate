from api.core import BaseModel
from extensions import db


class App(BaseModel):
    __tablename__ = "apps"
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
