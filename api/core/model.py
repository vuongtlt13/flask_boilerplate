from datetime import datetime
from sqlalchemy import inspect
from extensions import db


class TimestampMixin:
    created_at = db.Column(db.TIMESTAMP, default=datetime.now)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.now, onupdate=datetime.now)


class SerializerMixin:
    __hidden_columns__ = []

    def as_dict(self):
        result = {}
        for c in self.__table__.columns:
            if c.name in self.__hidden_columns__ or c in self.__hidden_columns__:
                continue
            value = getattr(self, c.name)
            if isinstance(value, datetime):
                value = value.isoformat()

            result[c.name] = value
        return result


class BaseModel(db.Model, TimestampMixin, SerializerMixin):
    __abstract__ = True

    @classmethod
    def primary_key(cls) -> str:
        return inspect(cls).primary_key[0].name
