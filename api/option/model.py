"""
    Author: Do Quoc Vuong
    Email: vuongtlt13@gmail.com
    Country: VietNam
    Generated by VGenerator
    Created at: 2021-06-15 10:23:12.531617Z
"""

from api.core import BaseModel
from extensions import db


class Option(BaseModel):
    __tablename__ = "options"
    __table_args__ = {
        'extend_existing': True
    }
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    description = db.Column(db.Text, nullable=False)
    unit_price = db.Column(db.BigInteger, nullable=False)
    unit_amount = db.Column(db.BigInteger, nullable=False, server_default='1')
