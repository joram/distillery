from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit, send

app = Flask(__name__)
CORS(app)
socket = SocketIO(app)


@socket.on('connect', namespace="dsf")
def on_connect():
    print('user connected')
    emit('float_sensor', {"name": "poop", "floating": True}, broadcast=True)

#
# @socket.on('activate_user')
# def on_active_user(data):
#     user = data.get('username')
#     emit('user_activated', {'user': user}, broadcast=True)
#
#
# @socket.on('deactivate_user')
# def on_inactive_user(data):
#     user = data.get('username')
#     emit('user_deactivated', {'user': user}, broadcast=True)
#
#
# @socket.on('join_room')
# def on_join(data):
#     room = data['room']
#     # join_room(room)
#     emit('open_room', {'room': room}, broadcast=True)
#
#
# @socket.on('send_message')
# def on_chat_sent(data):
#     room = data['room']
#     emit('message_sent', data, room=room)
#

@app.route("/")
def home():
    send("hello")
    return "hi"


# @socket.on('message', namespace="")
# def handle_message(message):
#     send(message)
#     print("handling message:", message)


if __name__ == '__main__':
    socket.run(app)

