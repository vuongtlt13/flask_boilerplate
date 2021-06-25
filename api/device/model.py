"""
    Author: Do Quoc Vuong
    Email: vuongtlt13@gmail.com
    Country: VietNam
    Generated by VGenerator
    Created at: 2021-06-15 10:23:12.528991Z
"""

from api.core import BaseModel
from extensions import db


class Device(BaseModel):
    __tablename__ = "devices"
    __table_args__ = {
        'extend_existing': True
    }
    id = db.Column(db.String(45), primary_key=True)
    license_id = db.Column(db.BigInteger, db.ForeignKey('licenses.id'), nullable=False, index=True)
    name = db.Column(db.String(100))
    ip_address = db.Column(db.String(45))
    country = db.Column(db.String(100))
    city = db.Column(db.String(100))
    last_active_at = db.Column(db.DateTime)
    device_info = db.Column(db.Text)
    license = db.relationship('License', primaryjoin='Device.license_id == License.id', backref='devices')