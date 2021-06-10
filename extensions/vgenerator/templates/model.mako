<%include file="header.mako"/>

from api.core import BaseModel
%if is_auth_model:
from extensions import db, jwt
% else:
from extensions import db
%endif


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


%if is_auth_model:
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return ${class_name}.query.filter_by(id=identity).one_or_none()
%endif