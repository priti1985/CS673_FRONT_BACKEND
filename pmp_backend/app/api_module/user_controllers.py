import datetime
from functools import wraps, update_wrapper
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from flask import Blueprint, render_template, flash, g, session, \
    redirect, url_for, Flask, request, jsonify, make_response
from werkzeug.security import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db
from flask_cors import CORS

# Import module models (i.e. User)
from app.api_module.models import User

# Define the blueprint: 'api', set its url prefix: app.url/${path}
api_mod = Blueprint('api', __name__, url_prefix='/api')

from app import app

CORS(app, resources={r"*": {"origins": "*"}})

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


# Set the route and accepted methods
@api_mod.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the rest api for the software engineering, BU-Spring-2019-Team-2'}), 200


@api_mod.route('/doc/', methods=['GET'])
def doc():
    return render_template("docstring.html")


@api_mod.route('/user/', methods=['POST'])
@token_required
def create_user(current_user):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')
    name = data['name']
    email = data['email']
    profile = data['profile']
    admin = data['admin']
    skills = ','.join(data['skills'])
    new_user = User(name=name, email=email, password=hashed_password, admin=admin, profile=profile, skills=skills)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New user created!'})


@api_mod.route('/user/', methods=['GET'])
@token_required
def get_all_users(current_user):

    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['id'] = user.id
        user_data['name'] = user.name
        user_data['email'] = user.email
        output.append(user_data)

    return jsonify({'users': output})


@api_mod.route('/user/<user_id>/', methods=['GET'])
@token_required
def get_one_user(current_user, user_id):

    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({'message': 'No user found!'})

    user_data = {}
    user_data['id'] = user.id
    user_data['name'] = user.name
    user_data['email'] = user.email
    user_data['password'] = user.password
    user_data['admin'] = user.admin

    return jsonify({'user': user_data})


@api_mod.route('/user/<user_id>/', methods=['DELETE'])
@token_required
def delete_user(current_user, user_id):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({'message': 'No user found!'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'The user has been deleted!'})


@api_mod.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    auth ={}
    auth['username'] = data['username']
    auth['password'] = data['password']

    if not auth or not auth['username'] or not auth['password']:
        return make_response(jsonify({'message': 'Could not verify'}), 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = User.query.filter_by(email=auth['username']).first()

    if not user:
        return make_response(jsonify({'message': 'Could not verify'}), 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth['password']):
        exp_date = datetime.datetime.utcnow() + datetime.timedelta(minutes=360000)
        token = jwt.encode({'id': user.id, 'exp': exp_date}, app.config['SECRET_KEY'])
        out = jsonify({'username': auth['username'], 'token': token.decode('UTF-8'), 'expiration date': exp_date})
        return out

    return make_response(jsonify({'message': 'Could not verify'}), 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
