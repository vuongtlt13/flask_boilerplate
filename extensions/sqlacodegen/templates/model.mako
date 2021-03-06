from api.core import BaseModel
from extensions import db


class ${class_name}(BaseModel):
    __tablename__ = "${table_name}"
    ${columns}
    ${hidden_columns if hidden_columns else "\n"}
    ${relationships if relationships else "\n"}