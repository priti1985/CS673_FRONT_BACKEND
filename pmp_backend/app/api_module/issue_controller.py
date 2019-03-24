from flask import Blueprint, jsonify, request

# Import the token_required for auth
from app.api_module.user_controllers import token_required

# Import the database object from the main app module
from app import db
from app.api_module.helpers import parse_date
from datetime import  datetime

# Import module models (i.e. Team)
from app.api_module.models import Issue, Employee, Project, IssueTracking

# Define the blueprint: 'api', set its url prefix: app.url/${path}
issue_mod = Blueprint('issue', __name__, url_prefix='/api/issue')


@issue_mod.route('/', methods=['POST'])
@token_required
def create_issue(current_user):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'}), 401

    data = request.get_json()
    name = data.get('name')
    start_date = parse_date(data.get('start_date', ''))
    due_date = parse_date(data.get('due_date', ''))
    status = data.get('status')
    priority = data.get('priority', 'medium')
    project = Project.query.filter_by(id=data.get('project_id')).first()
    employee = Employee.query.filter_by(id=data.get('employee_id')).first()

    if not project or not employee or not start_date or not due_date or not name:
        return jsonify({'message': 'No employee | sprint | start_date | due_date | name found with your inputs'}), 400
    json_issue = {'name': name, 'start_date': start_date, 'due_date': due_date, 'status': status,
                  'project': project, 'employee': employee, 'priority': priority}
    new_issue = Issue(json_issue=json_issue)
    db.session.add(new_issue)
    db.session.flush()
    id_ = new_issue.id
    db.session.commit()

    return jsonify({'message': 'New Issue created!', 'id': id_})


@issue_mod.route('/<issue_id>/', methods=['PUT'])
@token_required
def update_issue(current_user, issue_id):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    issue = Issue.query.filter_by(id=issue_id).first()
    if not issue:
        return jsonify({'message': 'No Issue found with your inputs'})
    data = request.get_json()
    if 'new_stage' in data:
        # add a tracking on the issue
        comment = 'moved from '+issue.status+' to '+data.get('new_stage')
        employee = Employee.query.filter_by(id=1).first()
        json_issue_tracking = {'date': datetime.now(), 'comment': comment, 'issue': issue, 'employee': employee}
        issue_tracking = IssueTracking(json_issue_tracking)
        issue.status = data.get('new_stage')
        db.session.add(issue_tracking)
    else:
        name = data.get('name')
        start_date = parse_date(data.get('start_date', ''))
        due_date = parse_date(data.get('due_date', ''))
        status = data.get('status')
        priority = data.get('priority', 'medium')
        project = Project.query.filter_by(id=data.get('project_id')).first()
        employee = Employee.query.filter_by(id=data.get('employee_id')).first()

        json_issue = {'name': name, 'start_date': start_date, 'due_date': due_date, 'status': status,
                      'project': project, 'employee': employee, 'priority': priority}
        issue.update(json_issue=json_issue)
    db.session.merge(issue)
    db.session.commit()

    return jsonify({'message': 'Issue Updated!'})


@issue_mod.route('/', methods=['GET'])
@token_required
def get_all_issues(current_user):

    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    issues = Issue.query.all()
    output = []

    datetimeFormat = '%Y-%m-%d %H:%M:%S'
    today = datetime.now()

    for issue in issues:
        issue_data = {}
        issue_data['id'] = issue.id
        issue_data['name'] = issue.name
        issue_data['start_date'] = issue.start_date
        issue_data['due_date'] = issue.due_date
        due_date = datetime.strptime(str(issue.due_date), datetimeFormat)
        diff = due_date - today
        remaining = str(diff.days)+' d '+str(round(diff.seconds / 60, 0))+' mn'
        issue_data['remaining'] = remaining
        issue_data['status'] = issue.status
        issue_data['priority'] = issue.priority
        issue_data['project'] = {'id': issue.project.id, 'name': issue.project.name}
        issue_data['employee'] = {'id': issue.employee.id, 'name': issue.employee.user.name}
        output.append(issue_data)

    return jsonify({'issues': output})


@issue_mod.route('/<issue_id>/', methods=['GET'])
@token_required
def get_one_issue(current_user, issue_id):

    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    issue = Issue.query.filter_by(id=issue_id).first()

    if not issue:
        return jsonify({'message': 'No Issue found!'})

    datetimeFormat = '%Y-%m-%d %H:%M:%S'
    today = datetime.now()

    issue_data = {}
    issue_data['id'] = issue.id
    issue_data['name'] = issue.name
    issue_data['start_date'] = issue.start_date
    issue_data['due_date'] = issue.due_date
    due_date = datetime.strptime(str(issue.due_date), datetimeFormat)
    diff = due_date - today
    remaining = str(diff.days) + ' d ' + str(round(diff.seconds / 60, 0)) + ' mn'
    issue_data['remaining'] = remaining
    issue_data['status'] = issue.status
    issue_data['priority'] = issue.priority
    issue_data['project'] = {'id': issue.project.id, 'name': issue.project.name}
    issue_data['employee'] = {'id': issue.employee.id, 'name': issue.employee.user.name}
    issue_data['tracking'] = [{'id': tracking.id, 'date': tracking.date, 'comment': tracking.comment,
                              'employee_id': tracking.employee.id, 'employee_name': tracking.employee.user.name}
                              for tracking in issue.issue_tracking]

    return jsonify({'issue': issue_data})


@issue_mod.route('/project/<project_id>/', methods=['GET'])
@token_required
def get_all_issues_of_a_project(current_user, project_id):

    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    issues = Issue.query.filter_by(project_id=project_id)
    output = []

    for issue in issues:
        issue_data = {}
        issue_data['id'] = issue.id
        issue_data['name'] = issue.name
        issue_data['start_date'] = issue.start_date
        issue_data['due_date'] = issue.due_date
        issue_data['status'] = issue.status
        issue_data['priority'] = issue.priority
        issue_data['project'] = {'id': issue.project.id, 'name': issue.project.name}
        issue_data['employee'] = {'id': issue.employee.id, 'name': issue.employee.user.name}
        output.append(issue_data)

    return jsonify({'issues': output})


@issue_mod.route('/project/<project_id>/<status>', methods=['GET'])
@token_required
def get_all_issues_of_a_project_with_status(current_user, project_id, status):

    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    issues = Issue.query.filter_by(project_id=project_id, status=status)
    output = []

    for issue in issues:
        issue_data = {}
        issue_data['id'] = issue.id
        issue_data['name'] = issue.name
        issue_data['start_date'] = issue.start_date
        issue_data['due_date'] = issue.due_date
        issue_data['status'] = issue.status
        issue_data['priority'] = issue.priority
        issue_data['sprint'] = {'id': issue.project.id, 'name': issue.project.name}
        issue_data['employee'] = {'id': issue.employee.id, 'name': issue.employee.user.name}
        output.append(issue_data)

    return jsonify({'issues': output})


@issue_mod.route('/employee/<employee_id>/', methods=['GET'])
@token_required
def get_all_issues_of_one_employee(current_user, employee_id):

    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    issues = Issue.query.filter_by(employee_id=employee_id)
    output = []

    for issue in issues:
        issue_data = {}
        issue_data['id'] = issue.id
        issue_data['name'] = issue.name
        issue_data['start_date'] = issue.start_date
        issue_data['due_date'] = issue.due_date
        issue_data['status'] = issue.status
        issue_data['priority'] = issue.priority
        issue_data['project'] = {'id': issue.project.id, 'name': issue.project.name}
        issue_data['employee'] = {'id': issue.employee.id, 'name': issue.employee.user.name}
        issue_data['tracking'] = [{'id': tracking.id, 'date': tracking.date, 'comment': tracking.comment,
                                   'employee_id': tracking.employee.id, 'employee_name': tracking.employee.user.name}
                                  for tracking in issue.issue_tracking]
        output.append(issue_data)

    return jsonify({'issues': output})


@issue_mod.route('/employee/<employee_id>/<status>/', methods=['GET'])
@token_required
def get_all_issues_of_one_employee_with_status(current_user, employee_id, status):

    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    issues = Issue.query.filter_by(employee_id=employee_id, status=status)
    output = []

    for issue in issues:
        task_data = {}
        task_data['id'] = issue.id
        task_data['name'] = issue.name
        task_data['start_date'] = issue.start_date
        task_data['due_date'] = issue.due_date
        task_data['status'] = issue.status
        task_data['priority'] = issue.priority
        task_data['project'] = {'id': issue.project.id, 'name': issue.project.name}
        task_data['employee'] = {'id': issue.employee.id, 'name': issue.employee.user.name}
        task_data['tracking'] = [{'id': tracking.id, 'date': tracking.date, 'comment': tracking.comment,
                                  'employee_id': tracking.employee.id, 'employee_name': tracking.employee.user.name}
                                 for tracking in issue.issue_tracking]
        output.append(task_data)

    return jsonify({'issues': output})


@issue_mod.route('/tracking/<issue_id>/', methods=['POST'])
@token_required
def create_new_tracking_on_a_task(current_user, issue_id):

    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    data = request.get_json()
    date = datetime.now()
    comment = data.get('comment')
    issue = Issue.query.filter_by(id=issue_id).first()
    employee = Employee.query.filter_by(id=data.get('employee_id')).first()

    if not issue or not employee:
        return jsonify({'message': 'No employee | issue found with your inputs'}), 404
    json_issue_tracking = {'date': date, 'comment': comment, 'issue': issue, 'employee': employee}
    new_issue_tracking = IssueTracking(json_issue_tracking=json_issue_tracking)
    db.session.add(new_issue_tracking)
    db.session.commit()

    return jsonify({'message': 'New IssueTracking created!'})


@issue_mod.route('/tracking/<issue_tracking_id>/', methods=['DELETE'])
@token_required
def delete_tracking_on_a_issue(current_user, issue_tracking_id):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'}), 401

    issue_tracking = IssueTracking.query.filter_by(id=issue_tracking_id).first()

    if not issue_tracking:
        return jsonify({'message': 'No issue_tracking found!'}), 404

    db.session.delete(issue_tracking)
    db.session.commit()

    return jsonify({'message': 'The tracking message has been deleted on the issue!'})
