# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db
from datetime import datetime


class Base(db.Model):
    """
       Define a base model for other database tables to inherit
    """
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class User(Base):
    """
        Define a User model
        name : <string> The name of the user
        email : <string> The email of the user; will also be used as username for login, auth,...
        password : <string> The password of the user
        profile : <string> The profile or brief description of the user
        skills : <list> list of skills of the user
        admin : <boolean> to precise if the user is an admin or not
    """
    __tablename__ = 'user'

    # User Name
    name = db.Column(db.String(128),  nullable=False)
    # Identification Data: email & password
    email = db.Column(db.String(128),  nullable=False, unique=True)
    password = db.Column(db.String(255),  nullable=False)
    # Authorisation Data: role & status
    profile = db.Column(db.String(128), nullable=False)
    skills = db.Column(db.String(128), nullable=False)
    admin = db.Column(db.Boolean, nullable=False)

    # New instance instantiation procedure
    def __init__(self, name, email, password, profile, skills, admin):
        self.name = name
        self.email = email
        self.password = password
        self.profile = profile
        self.skills = skills
        self.admin = admin

    def __repr__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class Employee(db.Model):
    """
        Define a the Employee model
        badge : <string> the badge number of the employee
        start_date : <datetime> the starting date of the user as an employee at a company
        end_date : <datetime> the probable ending date of the user as employee in a company
        is_full_time : <boolean> to precise if the employee is full time or not
        user : <User> The user from which we create the employee
        company : <Company> The company to which the employee belong
        role : <Role> The role of the employee on the company
        team : <Team> The team to which the employee belong
    """
    __tablename__ = 'employee'

    __table_args__ = (
        db.UniqueConstraint('badge', 'company_id', name='unique_badge_per_company'),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    badge = db.Column(db.String(150), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=True)
    is_full_time = db.Column(db.Boolean, nullable=False)

    # 1 to 1 relationship with user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('employee', lazy=True))

    # 1 to n relationship with company
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    company = db.relationship('Company', backref=db.backref('employee', lazy=True))

    # 1 to 1 relationship with role
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    role = db.relationship('Role', backref=db.backref('employee', lazy=True))

    # 1 to 1 relationship with Team
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    team = db.relationship('Team', backref=db.backref('employee', lazy=True))

    def __init__(self, json_employee):
        self.badge = json_employee.get('badge', '')
        self.start_date = json_employee.get('start_date', datetime.now())
        self.end_date = json_employee.get('end_date', None)
        self.is_full_time = json_employee.get('is_full_time', False)
        self.user = json_employee.get('user', None)
        self.company = json_employee.get('company', None)
        self.role = json_employee.get('role', None)
        self.team = json_employee.get('team')

    def __repr__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class Team(db.Model):
    __tablename__ = 'team'

    __table_args__ = (
        db.UniqueConstraint('name', 'company_id', name='unique_team_name_per_company'),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(192), nullable=False)
    comment = db.Column(db.Text, nullable=True)

    # 1 to n relationship with company
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    company = db.relationship('Company', backref=db.backref('team', lazy=True))

    def __init__(self, json_team):
        self.name = json_team.get('name')
        self.comment = json_team.get('comment')
        self.company = json_team.get('company')

    def __repr__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(192), nullable=False)
    comment = db.Column(db.Text, nullable=True)

    def __init__(self, json_role):
        self.name = json_role.get('name')
        self.comment = json_role.get('comment')

    def __repr__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class Company(db.Model):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(192), nullable=False, unique=True)
    comment = db.Column(db.Text, nullable=True)

    def __init__(self, json_company):
        self.name = json_company.get('name')
        self.comment = json_company.get('comment')

    def __repr__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class Project(db.Model):
    __tablename__ = 'project'

    __table_args__ = (
        db.UniqueConstraint('name', 'company_id', name='unique_project_name_per_company'),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(192), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    comment = db.Column(db.Text, nullable=True)

    # 1 to n relationship with company
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    company = db.relationship('Company', backref=db.backref('project', lazy=True))

    def __init__(self, json_project):
        self.name = json_project.get('name')
        self.start_date = json_project.get('start_date', datetime.now())
        self.due_date = json_project.get('due_date', datetime.now())
        self.comment = json_project.get('comment', None)
        self.company = json_project.get('company', None)

    def __repr__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class Sprint(db.Model):
    __tablename__ = 'sprint'

    __table_args__ = (
        db.UniqueConstraint('name', 'project_id', name='unique_sprint_name_per_project'),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(192), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    comment = db.Column(db.Text, nullable=True)

    # 1 to n relationship with user
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    project = db.relationship('Project', backref=db.backref('sprint', lazy=True))

    def __init__(self, json_sprint):
        self.name = json_sprint.get('name')
        self.start_date = json_sprint.get('start_date', datetime.now())
        self.due_date = json_sprint.get('due_date', datetime.now())
        self.comment = json_sprint.get('comment')
        self.project = json_sprint.get('project')

    def __repr__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class Issue(db.Model):
    __tablename__ = 'issue'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(192), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(192), nullable=False)
    priority = db.Column(db.String(192), nullable=False)
    # 1 to 1 relationship with user
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    project = db.relationship('Project', backref=db.backref('issue', lazy=True))

    # 1 to 1 relationship with user
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    employee = db.relationship('Employee', backref=db.backref('issue', lazy=True))

    def __init__(self, json_issue):
        self.name = json_issue.get('name')
        self.start_date = json_issue.get('start_date', datetime.now())
        self.due_date = json_issue.get('due_date', datetime.now())
        self.status = json_issue.get('status')
        self.project = json_issue.get('project', None)
        self.employee = json_issue.get('employee', None)
        self.priority = json_issue.get('priority', 'medium')

    def update(self, json_issue):
        self.name = json_issue.get('name')
        self.start_date = json_issue.get('start_date', datetime.now())
        self.due_date = json_issue.get('due_date', datetime.now())
        self.status = json_issue.get('status')
        self.project = json_issue.get('project', None)
        self.employee = json_issue.get('employee', None)
        self.priority = json_issue.get('priority', 'medium')

    def __repr__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class IssueTracking(db.Model):
    __tablename__ = 'issue_tracking'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    comment = db.Column(db.Text, nullable=True)

    # 1 to 1 relationship with issue
    issue_id = db.Column(db.Integer, db.ForeignKey('issue.id'), nullable=False)
    issue = db.relationship('Issue', backref=db.backref('issue_tracking'))

    # 1 to 1 relationship with employee
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=True)
    employee = db.relationship('Employee', backref=db.backref('issue_tracking', lazy=True))

    def __init__(self, json_issue_tracking):
        self.date = json_issue_tracking.get('date')
        self.comment = json_issue_tracking.get('comment')
        self.issue = json_issue_tracking.get('issue')
        self.employee = json_issue_tracking.get('employee')

    def __repr__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class Task(db.Model):
    __tablename__ = 'task'

    __table_args__ = (
        db.UniqueConstraint('name', 'sprint_id', name='unique_task_name_per_sprint'),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(192), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(192), nullable=False)
    priority = db.Column(db.String(192), nullable=False)

    # 1 to 1 relationship with Sprint
    sprint_id = db.Column(db.Integer, db.ForeignKey('sprint.id'), nullable=False)
    sprint = db.relationship('Sprint', backref=db.backref('task', lazy=True))

    # 1 to 1 relationship with employee
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    employee = db.relationship('Employee', backref=db.backref('task', lazy=True, uselist=False))

    def __init__(self, json_task):
        self.name = json_task.get('name')
        self.start_date = json_task.get('start_date', datetime.now())
        self.due_date = json_task.get('due_date', datetime.now())
        self.status = json_task.get('status')
        self.sprint = json_task.get('sprint')
        self.employee = json_task.get('employee')
        self.priority = json_task.get('priority', 'medium')

    def update(self, json_task):
        self.name = json_task.get('name')
        self.start_date = json_task.get('start_date', datetime.now())
        self.due_date = json_task.get('due_date', datetime.now())
        self.status = json_task.get('status')
        self.sprint = json_task.get('sprint')
        self.employee = json_task.get('employee')
        self.priority = json_task.get('priority', 'medium')

    def __repr__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class TaskTracking(db.Model):
    __tablename__ = 'task_tracking'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    comment = db.Column(db.Text, nullable=True)

    # 1 to n relationship with task
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    task = db.relationship('Task', backref=db.backref('task_tracking'))

    # 1 to 1 relationship with employee
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    employee = db.relationship('Employee', backref=db.backref('task_tracking', lazy=True, uselist=False))

    def __init__(self, json_task_tracking):
        self.date = json_task_tracking.get('date', datetime.now())
        self.comment = json_task_tracking.get('comment', None)
        self.task = json_task_tracking.get('task', None)
        self.employee = json_task_tracking.get('employee', None)

    def __repr__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


# the many to many relationship between employee and chatroom
employee_chatroom = db.Table('employee_chatroom',
                             db.Column('employee_id', db.Integer, db.ForeignKey('employee.id'), primary_key=True),
                             db.Column('chatroom_id', db.Integer, db.ForeignKey('chat_room.id'), primary_key=True)
                             )


class ChatRoom(db.Model):
    __tablename__ = 'chat_room'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(192), nullable=False)
    # Direct Message (DM) or Group will be hold by the type, this will help avoid having many DM for same pair of users
    type = db.Column(db.String(192), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    employees = db.relationship('Employee', secondary=employee_chatroom, lazy='subquery',
                                backref=db.backref('chat_room', lazy=True))

    def __init__(self, json_chat_room):
        self.name = json_chat_room.get('name')
        self.type = json_chat_room.get('type')
        self.start_date = json_chat_room.get('start_date', datetime.now())

    def __repr__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class Message(db.Model):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.Text, nullable=True)
    sending_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # 1 to 1 relationship with ChatRoom
    chatroom_id = db.Column(db.Integer, db.ForeignKey('chat_room.id'), nullable=False)
    chatroom = db.relationship('ChatRoom', backref=db.backref('message', lazy=True, uselist=False))

    # 1 to 1 relationship with employee
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    employee = db.relationship('Employee', backref=db.backref('message', lazy=True, uselist=False))

    def __init__(self, json_message):
        self.message = json_message.get('message', None)
        self.sending_date = json_message.get('sending_date', datetime.now())
        self.chatroom = json_message.get('chatroom')
        self.employee = json_message.get('employee')

    def __repr__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

