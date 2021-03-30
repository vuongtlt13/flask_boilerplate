<%include file="header.mako"/>

from api.core import BaseModel
from extensions import db


class ${class_name}(BaseModel):
    __tablename__ = "${table_name}"
% for column in columns:
    ${column}
% endfor
% for hidden_column in hidden_columns:
    ${hidden_column}
% endfor
% for relationship in relationships:
    ${relationship}
% endfor