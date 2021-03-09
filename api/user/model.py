from api.core import BaseModel
from extensions import db


class User(BaseModel):
    __tablename__ = "users"
    id = db.Column(db.BigInteger, primary_key=True)
    service_id = db.Column(db.BigInteger, db.ForeignKey('services.id'), nullable=False, index=True)
    username = db.Column(db.String(45), nullable=False, unique=True)
    password = db.Column(db.String(45), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, server_default='1')
    service = db.relationship('Service', primaryjoin='User.service_id == Service.id', backref='users')
