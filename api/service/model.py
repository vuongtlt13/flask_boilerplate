from api.core import BaseModel
from extensions import db


class Service(BaseModel):
    __tablename__ = "services"
    id = db.Column(db.BigInteger, primary_key=True)
    app_id = db.Column(db.BigInteger, db.ForeignKey('apps.id'), nullable=False, index=True)
    company_id = db.Column(db.BigInteger, db.ForeignKey('companies.id'), nullable=False, index=True)
    is_active = db.Column(db.Boolean, nullable=False, server_default='1')
    app = db.relationship('App', primaryjoin='Service.app_id == App.id', backref='services')
    company = db.relationship('Company', primaryjoin='Service.company_id == Company.id', backref='services')
