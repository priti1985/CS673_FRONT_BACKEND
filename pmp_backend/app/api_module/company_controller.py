from flask import Blueprint, jsonify, request

# Import the token_required for auth
from app.api_module.user_controllers import token_required

# Import the database object from the main app module
from app import db

# Import module models (i.e. Company)
from app.api_module.models import Company

# Define the blueprint: 'api', set its url prefix: app.url/${path}
company_mod = Blueprint('company', __name__, url_prefix='/api/company')


@company_mod.route('/', methods=['POST'])
@token_required
def create_company(current_user):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    data = request.get_json()
    name = data.get('name')
    comment = data.get('comment', None)

    json_company = {'name': name, 'comment': comment}
    new_company = Company(json_company=json_company)
    db.session.add(new_company)
    db.session.commit()

    return jsonify({'message': 'New Company created!'})


@company_mod.route('/', methods=['GET'])
@token_required
def get_all_company(current_user):

    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    companies = Company.query.all()
    output = []

    for company in companies:
        company_data = {}
        company_data['id'] = company.id
        company_data['name'] = company.name
        output.append(company_data)

    return jsonify({'companies': output})


@company_mod.route('/<company_id>/', methods=['GET'])
@token_required
def get_one_company(current_user, company_id):

    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    company = Company.query.filter_by(id=company_id).first()

    if not company:
        return jsonify({'message': 'No Company found!'})

    company_data = {}
    company_data['id'] = company.id
    company_data['name'] = company.name
    company_data['comment'] = company.comment

    return jsonify({'company': company_data})
