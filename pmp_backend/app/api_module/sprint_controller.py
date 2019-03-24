from flask import Blueprint, jsonify, request

# Import the token_required for auth
from app.api_module.user_controllers import token_required

# Import the database object from the main app module
from app import db
from app.api_module.helpers import parse_date

# Import module models (i.e. Role)
from app.api_module.models import Project, Sprint

# Define the blueprint: 'api', set its url prefix: app.url/${path}
sprint_mod = Blueprint('sprint', __name__, url_prefix='/api/sprint')


@sprint_mod.route('/', methods=['POST'])
@token_required
def create_sprint(current_user):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    data = request.get_json()
    name = data.get('name')
    start_date = parse_date(data.get('start_date', ''))
    due_date = parse_date(data.get('due_date', ''))
    comment = data.get('comment', None)
    project = Project.query.filter_by(id=data.get('project_id')).first()

    json_sprint = {'name': name, 'start_date': start_date, 'due_date': due_date, 'comment': comment, 'project': project}
    new_sprint = Sprint(json_sprint=json_sprint)
    db.session.add(new_sprint)
    db.session.commit()

    return jsonify({'message': 'New sprint created!'})


@sprint_mod.route('/', methods=['GET'])
@token_required
def get_all_sprints(current_user):

    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    sprints = Sprint.query.all()
    output = []

    for sprint in sprints:
        sprint_data = {}
        sprint_data['id'] = sprint.id
        sprint_data['name'] = sprint.name
        sprint_data['project'] = {'id': sprint.project.id, 'name': sprint.project.name}
        output.append(sprint_data)

    return jsonify({'sprints': output})


@sprint_mod.route('/<sprint_id>/', methods=['GET'])
@token_required
def get_one_sprint(current_user, sprint_id):

    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    sprint = Sprint.query.filter_by(id=sprint_id).first()

    if not sprint:
        return jsonify({'message': 'No sprint found!'})

    sprint_data = {}
    sprint_data['id'] = sprint.id
    sprint_data['name'] = sprint.name
    sprint_data['start_date'] = sprint.start_date
    sprint_data['due_date'] = sprint.due_date
    sprint_data['due_date'] = sprint.comment
    sprint_data['project'] = {'id': sprint.project.id, 'name': sprint.project.name}

    return jsonify({'sprint': sprint_data})


@sprint_mod.route('/project/<project_id>/', methods=['GET'])
@token_required
def get_all_sprints_of_a_project(current_user, project_id):

    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    sprints = Sprint.query.filter_by(company_id=project_id)
    output = []

    for sprint in sprints:
        sprint_data = {}
        sprint_data['id'] = sprint.id
        sprint_data['name'] = sprint.name
        sprint_data['start_date'] = sprint.start_date
        sprint_data['due_date'] = sprint.due_date
        sprint_data['due_date'] = sprint.comment
        sprint_data['project'] = {'id': sprint.project.id, 'name': sprint.project.name}
        output.append(sprint_data)

    return jsonify({'sprints': output})

