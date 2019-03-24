from flask import Blueprint, jsonify, request
from flask_socketio import SocketIO, emit

# Import the token_required for auth
from app.api_module.user_controllers import token_required

# Import the database object from the main app module
from app import db, app


# Import module models (i.e. ChatRoom, Message, Employee)
from app.api_module.models import ChatRoom, Message, Employee

# Define the blueprint: 'api', set its url prefix: app.url/${path}
chat_mod = Blueprint('chat', __name__, url_prefix='/api/chat')

socket_io = SocketIO(app)


@chat_mod.route('/room', methods=['POST'])
@token_required
def create_chat_room(current_user):
    if not current_user:
        return jsonify({'message': 'Cannot perform that function without login first!'}), 400

    data = request.get_json()
    name = data.get('name')
    chat_type = data.get('type', None)

    json_chat_room = {'name': name, 'type': chat_type}
    new_chat_room = ChatRoom(json_chat_room=json_chat_room)
    db.session.add(new_chat_room)
    db.session.commit()

    return jsonify({'message': 'New chat_room created!'})


@socket_io.on('my event')
def handle_my_custom_event(json):
    print('received data ', json)
    socket_io.emit('the response', json)

