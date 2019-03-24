from flask import Blueprint, jsonify, request

# Import the token_required for auth
from app.api_module.user_controllers import token_required

# Import the database object from the main app module
from app import db
from app.api_module.helpers import parse_date

# Import module models (i.e. Team)
from app.api_module.models import Employee, Team, Company, Role, User

# Define the blueprint: 'api', set its url prefix: app.url/${path}
employee_mod = Blueprint('employee', __name__, url_prefix='/api/employee')


@employee_mod.route('/', methods=['POST'])
@token_required
def create_employee(current_user):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'}), 401

    data = request.get_json()
    badge = data.get('badge')
    start_date = parse_date(data.get('start_date', ''))
    end_date = parse_date(data.get('end_date', ''))
    is_full_time = data.get('is_full_time')
    user = User.query.filter_by(id=data.get('user_id')).first()
    role = Role.query.filter_by(id=data.get('role_id')).first()
    team = Team.query.filter_by(id=data.get('team_id')).first()
    company = Company.query.filter_by(id=data.get('company_id')).first()

    if not company or not role or not team or not user:
        return jsonify({'message': 'No company | role | team | user found with your inputs ids'})
    json_employee = {'badge': badge, 'start_date': start_date, 'end_date': end_date,
                     'is_full_time': is_full_time, 'user': user, 'role': role, 'team': team, 'company': company}
    new_employee = Employee(json_employee=json_employee)
    db.session.add(new_employee)
    db.session.commit()

    return jsonify({'message': 'New Employee created!'})


@employee_mod.route('/', methods=['GET'])
@token_required
def get_all_employee(current_user):

    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'}), 401

    employees = Employee.query.all()
    output = []

    for employee in employees:
        employe_data = {}
        employe_data['id'] = employee.id
        employe_data['badge'] = employee.badge
        employe_data['name'] = employee.user.name
        employe_data['company_name'] = employee.company.name
        employe_data['is_full_time'] = employee.is_full_time
        output.append(employe_data)

    return jsonify({'employees': output})


@employee_mod.route('/<employee_id>/', methods=['GET'])
@token_required
def get_one_employee(current_user, employee_id):

    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'}), 401

    employee = Employee.query.filter_by(id=employee_id).first()

    if not employee:
        return jsonify({'message': 'No Employee found!'})

    employe_data = {}
    employe_data['id'] = employee.id
    employe_data['badge'] = employee.badge
    employe_data['is_full_time'] = employee.is_full_time
    employe_data['user'] = {'id': employee.user.id, 'name': employee.user.name}
    employe_data['company'] = {'id': employee.company.id, 'name': employee.company.name}
    employe_data['role'] = {'id': employee.role.id, 'name': employee.role.name}
    employe_data['team'] = {'id': employee.team.id, 'name': employee.team.name}

    return jsonify({'employee': employe_data})


@employee_mod.route('/company/<company_id>/', methods=['GET'])
@token_required
def get_all_employee_of_a_company(current_user, company_id):

    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'}), 401

    employees = Employee.query.filter_by(company_id=company_id)
    output = []

    for employee in employees:
        employe_data = {}
        employe_data['id'] = employee.id
        employe_data['badge'] = employee.badge
        employe_data['is_full_time'] = employee.is_full_time
        employe_data['user'] = {'id': employee.user.id, 'name': employee.user.name}
        employe_data['company'] = {'id': employee.company.id, 'name': employee.company.name}
        employe_data['role'] = {'id': employee.role.id, 'name': employee.role.name}
        employe_data['team'] = {'id': employee.team.id, 'name': employee.team.name}
        output.append(employe_data)

    return jsonify({'employees': output})


@employee_mod.route('/company/<company_id>/<team_id>/', methods=['GET'])
@token_required
def get_all_employee_of_a_team(current_user, company_id, team_id):

    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'}), 401

    employees = Employee.query.filter_by(company_id=company_id, team_id=team_id)
    output = []

    for employee in employees:
        employe_data = {}
        employe_data['id'] = employee.id
        employe_data['badge'] = employee.badge
        employe_data['is_full_time'] = employee.is_full_time
        employe_data['user'] = {'id': employee.user.id, 'name': employee.user.name}
        employe_data['company'] = {'id': employee.company.id, 'name': employee.company.name}
        employe_data['role'] = {'id': employee.role.id, 'name': employee.role.name}
        employe_data['team'] = {'id': employee.team.id, 'name': employee.team.name}
        output.append(employe_data)

    return jsonify({'employees': output})
