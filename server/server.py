import os
from threading import Lock
import random
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO

app = Flask(__name__, static_folder="../distillery/build")
CORS(app)
socket = SocketIO(app)
thread = None
thread_lock = Lock()


def emit_value_update(module_name, variable_name, variable_value):
    msg = {
        "module": module_name,
        "variable": variable_name,
        "value": variable_value,
    }
    print("emitting ", msg)
    socket.emit('value_update', msg, broadcast=True, namespace="")


def temperature():
    print("temperature thread")
    i = 0
    while True:
        val = float(random.choice(range(0, 1000)))/10
        socket.sleep(1)
        probe = ["temp1", "temp2", "temp3"][i % 3]
        emit_value_update("temperature_probes", probe, val)
        i += 1


# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    filepath = os.path.normpath(os.path.join(app.static_folder, path))
    print("serving %s" % filepath)

    if path != "" and os.path.exists(filepath):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


@socket.on('connect')
def on_connect():

    # background thread emitting state
    global thread
    with thread_lock:
        if thread is None:
            thread = socket.start_background_task(temperature)

    # initial state
    emit_value_update("coolant", "enabled", True)
    emit_value_update("wash_bilge", "enabled", False)
    emit_value_update("wash_bilge", "floating", True)
    emit_value_update("wash_bilge", "open", 50)


if __name__ == '__main__':
    # app.run(use_reloader=True, port=5000)
    socket.run(app, use_reloader=True, port=5000)


