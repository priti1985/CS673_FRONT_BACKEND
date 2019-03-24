# Import flask and template operators
from flask import Flask, render_template
from flask_cors import CORS, cross_origin


# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


# Import a module / component using its blueprint handler variable (api_module)
from app.api_module.user_controllers import api_mod as api_mod
from app.api_module.company_controller import company_mod as comp_mod
from app.api_module.role_controller import role_mod as role_mod
from app.api_module.team_controller import team_mod as team_mod
from app.api_module.employee_controller import employee_mod as employee_mod
from app.api_module.project_controller import project_mod as project_mod
from app.api_module.sprint_controller import sprint_mod as sprint_mod
from app.api_module.task_controller import task_mod as task_mod
from app.api_module.issue_controller import issue_mod as issue_mod
from app.api_module.chat_controller import chat_mod as chat_mod

# Register blueprint(s)
app.register_blueprint(api_mod)
app.register_blueprint(comp_mod)
app.register_blueprint(role_mod)
app.register_blueprint(team_mod)
app.register_blueprint(employee_mod)
app.register_blueprint(project_mod)
app.register_blueprint(sprint_mod)
app.register_blueprint(task_mod)
app.register_blueprint(issue_mod)
app.register_blueprint(chat_mod)
# app.register_blueprint(xyz_module)

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()


CORS(app)

