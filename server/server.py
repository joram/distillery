#!/usr/bin/env python3

try:
    from RPi import GPIO
    valve_calibrate = True
except:
    print("faking rpi")
    import fake_rpi
    import sys
    sys.modules['RPi'] = fake_rpi.RPi  # Fake RPi (GPIO)
    sys.modules['smbus'] = fake_rpi.smbus  # Fake smbus (I2C)
    valve_calibrate = False
import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO
import pins
from modules import Relay, Bilge, TemperatureProbe

app = Flask(__name__, static_folder="../distillery/build")
CORS(app)
socket = SocketIO(app)
module_instances = [
    Relay("coolant", pins.COOLANT_PUMP),
    Bilge("wash_bilge", 18, valve_calibrate=valve_calibrate),
    TemperatureProbe("probe 0", 0),
    TemperatureProbe("probe 1", 1),
    TemperatureProbe("probe 2", 2),
    TemperatureProbe("probe 3", 3),
    TemperatureProbe("probe 4", 4),
    TemperatureProbe("probe 5", 6),
    TemperatureProbe("probe 6", 5),
    TemperatureProbe("probe 7", 7),
]


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
    for module in module_instances:
        module.emit(socket)


if __name__ == '__main__':
    # app.run(use_reloader=True, port=5000)
    socket.run(app, use_reloader=True, port=5000)


