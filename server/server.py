from threading import Lock
import random
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

app = Flask(__name__)
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
    while True:
        val = float(random.choice(range(0, 1000)))/10
        socket.sleep(1)
        probe = random.choice(["temp1", "temp2", "temp3"])
        emit_value_update("temperature_probes", probe, val)


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
    socket.run(app)


