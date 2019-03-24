from flask import Blueprint, jsonify, request

# Import the token_required for auth
from app.api_module.user_controllers import token_required

# Import the database object from the main app module
from app import db
from app.api_module.helpers import parse_date
from datetime import  datetime

# Import module models (i.e. Team)
from app.api_module.models import Task, Employee, Sprint, TaskTracking

# Define the blueprint: 'api', set its url prefix: app.url/${path}
task_mod = Blueprint('task', __name__, url_prefix='/api/task')


@task_mod.route('/', methods=['POST'])
@token_required
def create_task(current_user):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    data = request.get_json()
    name = data.get('name')
    start_date = parse_date(data.get('start_date', ''))
    due_date = parse_date(data.get('due_date', ''))
    status = data.get('status')
    priority = data.get('priority', 'medium')
    sprint = Sprint.query.filter_by(id=data.get('sprint_id')).first()
    employee = Employee.query.filter_by(id=data.get('employee_id')).first()

    if not sprint or not employee or not start_date or not due_date or not name:
        return jsonify({'message': 'No employee | sprint | start_date | due_date | name found with your inputs'})
    json_task = {'name': name, 'start_date': start_date, 'due_date': due_date, 'status': status,
                 'sprint': sprint, 'employee': employee, 'priority': priority}
    new_task = Task(json_task=json_task)
    db.session.add(new_task)
    db.session.commit()

    return jsonify({'message': 'New Task created!'})


@task_mod.route('/<task_id>/', methods=['PUT'])
@token_required
def update_task(current_user, task_id):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    task = Task.query.filter_by(id=task_id).first()
    if not task:
        return jsonify({'message': 'No Task found with your inputs'})
    data = request.get_json()
    name = data.get('name')
    start_date = parse_date(data.get('start_date', ''))
    due_date = parse_date(data.get('due_date', ''))
    status = data.get('status')
    priority = data.get('priority', 'medium')
    sprint = Sprint.query.filter_by(id=data.get('sprint_id')).first()
    employee = Employee.query.filter_by(id=data.get('employee_id')).first()

    json_task = {'name': name, 'start_date': start_date, 'due_date': due_date, 'status': status,
                 'sprint': sprint, 'employee': employee, 'priority': priority}
    task.update(json_task=json_task)
    db.session.merge(task)
    db.session.commit()

    return jsonify({'message': 'Task Updated!'})


@task_mod.route('/', methods=['GET'])
@token_required
def get_all_task(current_user):

    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    tasks = Task.query.all()
    output = []

    for task in tasks:
        task_data = {}
        task_data['id'] = task.id
        task_data['name'] = task.name
        task_data['start_date'] = task.start_date
        task_data['due_date'] = task.due_date
        task_data['status'] = task.status
        task_data['priority'] = task.priority
        task_data['sprint'] = {'id': task.sprint.id, 'name': task.sprint.name}
        output.append(task_data)

    return jsonify({'tasks': output})


@task_mod.route('/<task_id>/', methods=['GET'])
@token_required
def get_one_task(current_user, task_id):

    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    task = Task.query.filter_by(id=task_id).first()

    if not task:
        return jsonify({'message': 'No Task found!'}), 404

    task_data = {}
    task_data['id'] = task.id
    task_data['name'] = task.name
    task_data['start_date'] = task.start_date
    task_data['due_date'] = task.due_date
    task_data['status'] = task.status
    task_data['priority'] = task.priority
    task_data['sprint'] = {'id': task.sprint.id, 'name': task.sprint.name}
    task_data['employee'] = {'id': task.employee.id, 'name': task.employee.user.name}
    task_data['tracking'] = [{'id': tracking.id, 'date': tracking.date, 'comment': tracking.comment,
                              'employee_id': tracking.employee.id, 'employee_name': tracking.employee.user.name}
                             for tracking in task.task_tracking]

    return jsonify({'task': task_data})


@task_mod.route('/sprint/<sprint_id>/', methods=['GET'])
@token_required
def get_all_task_of_a_sprint(current_user, sprint_id):

    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    tasks = Task.query.filter_by(sprint_id=sprint_id)
    output = []

    for task in tasks:
        task_data = {}
        task_data['id'] = task.id
        task_data['name'] = task.name
        task_data['start_date'] = task.start_date
        task_data['due_date'] = task.due_date
        task_data['status'] = task.status
        task_data['priority'] = task.priority
        task_data['sprint'] = {'id': task.sprint.id, 'name': task.sprint.name}
        task_data['employee'] = {'id': task.employee.id, 'name': task.employee.user.name}
        output.append(task_data)

    return jsonify({'tasks': output})


@task_mod.route('/sprint/<sprint_id>/<status>', methods=['GET'])
@token_required
def get_all_task_of_a_sprint_with_status(current_user, sprint_id, status):

    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    tasks = Task.query.filter_by(sprint_id=sprint_id, status=status)
    output = []

    for task in tasks:
        task_data = {}
        task_data['id'] = task.id
        task_data['name'] = task.name
        task_data['start_date'] = task.start_date
        task_data['due_date'] = task.due_date
        task_data['status'] = task.status
        task_data['priority'] = task.priority
        task_data['sprint'] = {'id': task.sprint.id, 'name': task.sprint.name}
        task_data['employee'] = {'id': task.employee.id, 'name': task.employee.user.name}
        output.append(task_data)

    return jsonify({'tasks': output})


@task_mod.route('/employee/<employee_id>/', methods=['GET'])
@token_required
def get_all_tasks_of_one_employee(current_user, employee_id):

    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    tasks = Task.query.filter_by(employee_id=employee_id)
    output = []

    for task in tasks:
        task_data = {}
        task_data['id'] = task.id
        task_data['name'] = task.name
        task_data['start_date'] = task.start_date
        task_data['due_date'] = task.due_date
        task_data['status'] = task.status
        task_data['priority'] = task.priority
        task_data['sprint'] = {'id': task.sprint.id, 'name': task.sprint.name}
        task_data['employee'] = {'id': task.employee.id, 'name': task.employee.user.name}
        task_data['tracking'] = [{'id': tracking.id, 'date': tracking.date, 'comment': tracking.comment,
                                  'employee_id': tracking.employee.id, 'employee_name': tracking.employee.user.name}
                                 for tracking in task.task_tracking]
        output.append(task_data)

    return jsonify({'tasks': output})


@task_mod.route('/employee/<employee_id>/<status>/', methods=['GET'])
@token_required
def get_all_tasks_of_one_employee_with_status(current_user, employee_id, status):

    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    tasks = Task.query.filter_by(employee_id=employee_id, status=status)
    output = []

    for task in tasks:
        task_data = {}
        task_data['id'] = task.id
        task_data['name'] = task.name
        task_data['start_date'] = task.start_date
        task_data['due_date'] = task.due_date
        task_data['status'] = task.status
        task_data['priority'] = task.priority
        task_data['sprint'] = {'id': task.sprint.id, 'name': task.sprint.name}
        task_data['employee'] = {'id': task.employee.id, 'name': task.employee.user.name}
        task_data['tracking'] = [{'id': tracking.id, 'date': tracking.date, 'comment': tracking.comment,
                                  'employee_id': tracking.employee.id, 'employee_name': tracking.employee.user.name}
                                 for tracking in task.task_tracking]
        output.append(task_data)

    return jsonify({'tasks': output})


@task_mod.route('/tracking/<task_id>/', methods=['POST'])
@token_required
def create_new_tracking_on_a_task(current_user, task_id):

    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    data = request.get_json()
    date = datetime.now()
    comment = data.get('comment')
    task = Task.query.filter_by(id=task_id).first()
    employee = Employee.query.filter_by(id=data.get('employee_id')).first()

    if not task or not employee:
        return jsonify({'message': 'No employee | task found with your inputs'})
    json_task_tracking = {'date': date, 'comment': comment, 'task': task, 'employee': employee}
    new_task_tracking = TaskTracking(json_task_tracking=json_task_tracking)
    db.session.add(new_task_tracking)
    db.session.commit()

    return jsonify({'message': 'New TaskTracking created!'})


@task_mod.route('/tracking/<task_tracking_id>/', methods=['DELETE'])
@token_required
def delete_tracking_on_a_task(current_user, task_tracking_id):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    task_tracking = TaskTracking.query.filter_by(id=task_tracking_id).first()

    if not task_tracking:
        return jsonify({'message': 'No task_tracking found!'})

    db.session.delete(task_tracking)
    db.session.commit()

    return jsonify({'message': 'The tracking message has been deleted on the task!'})
