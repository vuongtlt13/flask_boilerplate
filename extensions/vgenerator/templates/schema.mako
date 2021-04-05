from flask_restx import fields

from extensions import api
from extensions.response import PaginateResponseSchema, ResponseSchema, paginate_model

${singular_pascal_case_model_name}Schema = api.model('${singular_pascal_case_model_name}', {
% for column in return_columns:
    ${column},
% endfor
})

${singular_pascal_case_model_name}Response = api.clone('${singular_pascal_case_model_name}Response', ResponseSchema, {
    "data": fields.Nested(${singular_pascal_case_model_name}Schema, allow_null=True)
})

Create${singular_pascal_case_model_name}Request = api.model('Create${singular_pascal_case_model_name}Request', {
% for column in creatable_columns:
    ${column},
% endfor
})

Update${singular_pascal_case_model_name}Request = api.model('Update${singular_pascal_case_model_name}Request', {
% for column in updatable_columns:
    ${column},
% endfor
})

${singular_snake_case_model_name}_paginate_model = api.clone('${singular_snake_case_model_name}_paginate_model', paginate_model, {
    '${plural_snake_case_model_name}': fields.List(fields.Nested(${singular_pascal_case_model_name}Schema))
})

${singular_pascal_case_model_name}PaginateResponse = api.clone('${singular_pascal_case_model_name}PaginateResponse', PaginateResponseSchema, {
    'data': fields.Nested(${singular_snake_case_model_name}_paginate_model, allow_null=True),
})
