from api.core import BaseModel
from extensions import db


class ${class_name}(BaseModel):
    __tablename__ = "${table_name}"
    ${columns}
    ${(hidden_columns + "\n") if hidden_columns else "\n"}${"\t" + (relationships if relationships else "\n")}