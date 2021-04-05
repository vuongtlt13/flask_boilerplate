import abc
from typing import Any, Dict, Optional, Tuple
from sqlalchemy.exc import IntegrityError

from api.core import BaseModel
from extensions import db
from extensions.excpetion import DatabaseDuplicateException

DATABASE_DUPLICATE_ERROR_CODE = 1062


class BaseRepository:
    def __init__(self):
        self._model: BaseModel = self.model()

    @abc.abstractmethod
    def model(self):
        raise NotImplemented

    def find_by_id(self, _id) -> Optional[db.Model]:
        primary_column = self._model.primary_key()
        queries = {
            primary_column: _id
        }
        return self._model.query.filter_by(**queries).first()

    def create(self, data: Dict) -> Tuple[Optional[db.Model], Any]:
        try:
            new_record = self._model(**data)
            db.session.add(new_record)
            db.session.commit()
            return new_record, None
        except IntegrityError as e:
            if e.orig.args[0] == DATABASE_DUPLICATE_ERROR_CODE:
                raise DatabaseDuplicateException(str(e))
        except Exception as e:
            return None, str(e)

    def update(self, _id, data: Dict) -> Tuple[Optional[db.Model], Any]:
        record = self.find_by_id(_id=_id)
        if record is None:
            return record, "not_found"
        try:
            for key, value in data.items():
                setattr(record, key, value)
            db.session.commit()
            return record, None
        except Exception as e:
            return None, str(e)

    def delete(self, _id):
        primary_column = self._model.primary_key()
        queries = {
            primary_column: _id
        }
        result = self._model.query.filter_by(**queries).delete()
        db.session.commit()
        return result

    def get(self, page: int, size: int):
        result = self._model.query.offset((page - 1)*size).limit(size).all()
        return result

    def find_by_column(self, column: str, value):
        condition = {
            column: value
        }
        return self._model.query.filter_by(**condition).first()
