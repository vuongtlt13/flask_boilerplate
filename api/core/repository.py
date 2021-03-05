import abc
from typing import Dict, Optional

from extensions import db


class BaseRepository:
    def __init__(self):
        self._model = self.model()

    @abc.abstractmethod
    def model(self):
        raise NotImplemented

    def find_by_id(self, id) -> Optional[db.Model]:
        primary_column = self._model.primary_key()
        queries = {
            primary_column: id
        }
        return self._model.query.filter_by(**queries).first()

    def create(self, data: Dict) -> Optional[db.Model]:
        new_record = self._model(**data)
        db.session.add(new_record)
        db.session.commit()

        return new_record

    def update(self, id, data: Dict) -> Optional[db.Model]:
        record = self.find_by_id(id=id)
        if record is None:
            return record

        for key, value in data.items():
            setattr(record, key, value)
        db.session.commit()
        return record

    def delete(self, id):
        primary_column = self._model.primary_key()
        queries = {
            primary_column: id
        }
        result = self._model.query.filter_by(**queries).delete()
        db.session.commit()
        return result

    def get(self, page: int, size: int):
        result = self._model.query.offset((page - 1)*size).limit(size).all()
        return result
