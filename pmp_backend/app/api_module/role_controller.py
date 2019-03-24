from flask import Blueprint, jsonify, request

# Import the token_required for auth
from app.api_module.user_controllers import token_required

# Import the database object from the main app module
from app import db

# Import module models (i.e. Role)
from app.api_module.models import Role

# Define the blueprint: 'api', set its url prefix: app.url/${path}
role_mod = Blueprint('role', __name__, url_prefix='/api/role')


@role_mod.route('/', methods=['POST'])
@token_required
def create_role(current_user):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    data = request.get_json()
    name = data.get('name')
    comment = data.get('comment', None)

    json_role = {'name': name, 'comment': comment}
    new_role = Role(json_role=json_role)
    db.session.add(new_role)
    db.session.commit()

    return jsonify({'message': 'New Role created!'})


@role_mod.route('/', methods=['GET'])
@token_required
def get_all_roles(current_user):

    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    roles = Role.query.all()
    output = []

    for role in roles:
        role_data = {}
        role_data['id'] = role.id
        role_data['name'] = role.name
        output.append(role_data)

    return jsonify({'roles': output})


@role_mod.route('/<role_id>/', methods=['GET'])
@token_required
def get_one_role(current_user, role_id):

    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    role = Role.query.filter_by(id=role_id).first()

    if not role:
        return jsonify({'message': 'No role found!'})

    role_data = {}
    role_data['id'] = role.id
    role_data['name'] = role.name
    role_data['comment'] = role.comment

    return jsonify({'role': role_data})
