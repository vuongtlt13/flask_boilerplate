"""
    Author: Do Quoc Vuong
    Email: vuongtlt13@gmail.com
    Country: VietNam
    Generated by VGenerator
    Created at: 2021-06-11 17:52:02.900750Z
"""

from api.core import BaseModel
from extensions import db


class License(BaseModel):
    __tablename__ = "licenses"
    id = db.Column(db.BigInteger, primary_key=True)
    code = db.Column(db.String(100), nullable=False)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), nullable=False, index=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False, index=True)
    is_active = db.Column(db.Integer, nullable=False, server_default='0')
    actived_at = db.Column(db.DateTime)
    expired_at = db.Column(db.DateTime)
    application = db.relationship('Application', primaryjoin='License.application_id == Application.id', backref='licenses')
    user = db.relationship('User', primaryjoin='License.user_id == User.id', backref='licenses')
