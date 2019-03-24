from flask import Blueprint, jsonify, request

# Import the token_required for auth
from app.api_module.user_controllers import token_required

# Import the database object from the main app module
from app import db

# Import module models (i.e. Team)
from app.api_module.models import Team, Company

# Define the blueprint: 'api', set its url prefix: app.url/${path}
team_mod = Blueprint('team', __name__, url_prefix='/api/team')


@team_mod.route('/', methods=['POST'])
@token_required
def create_team(current_user):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    data = request.get_json()
    name = data.get('name')
    comment = data.get('comment', None)
    company = Company.query.filter_by(id=data.get('company_id')).first()

    if not company:
        return jsonify({'message': 'No Company found with id ' + str(data.get('company_id'))})
    json_team = {'name': name, 'comment': comment, 'company': company}
    new_team = Team(json_team=json_team)
    db.session.add(new_team)
    db.session.commit()

    return jsonify({'message': 'New Team created!'})


@team_mod.route('/', methods=['GET'])
@token_required
def get_all_teams(current_user):

    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    teams = Team.query.all()
    output = []

    for team in teams:
        team_data = {}
        team_data['id'] = team.id
        team_data['name'] = team.name
        output.append(team_data)

    return jsonify({'teams': output})


@team_mod.route('/<team_id>/', methods=['GET'])
@token_required
def get_one_team(current_user, team_id):

    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    team = Team.query.filter_by(id=team_id).first()

    if not team:
        return jsonify({'message': 'No Team found!'})

    team_data = {}
    team_data['id'] = team.id
    team_data['name'] = team.name
    team_data['comment'] = team.comment
    team_data['company'] = {'id': team.company.id,
                            'name': team.company.name}

    return jsonify({'team': team_data})
