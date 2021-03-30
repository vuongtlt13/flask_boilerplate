from flask_restx import fields

from extensions import api
from extensions.response import PaginateResponseSchema, ResponseSchema, paginate_model

CompanySchema = api.model('Company', {
    'id': fields.Integer(readOnly=True, required=True),
    'name': fields.String(readOnly=False, required=True),
})

CompanyResponse = api.clone('CompanyResponse', ResponseSchema, {
    "data": fields.Nested(CompanySchema)
})

CreateCompanyRequest = api.model('CreateCompanyRequest', {
    'name': fields.String(readOnly=False, required=True),
})

UpdateCompanyRequest = api.model('UpdateCompanyRequest', {
    'name': fields.String(readOnly=False, required=True),
})

company_paginate_model = api.clone('company_paginate_model', paginate_model, {
    'companies': fields.List(fields.Nested(CompanySchema))
})

CompanyPaginateResponse = api.clone('CompanyPaginateResponse', PaginateResponseSchema, {
    'data': fields.Nested(company_paginate_model),
})
