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
    fake_rpi.toggle_print(False)
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
    TemperatureProbe("probe 7", 1),
    TemperatureProbe("probe 2", 2),
    TemperatureProbe("probe 3", 3),
    TemperatureProbe("probe 4", 4),
    TemperatureProbe("probe 5", 6),
    TemperatureProbe("probe 6", 5),
#    TemperatureProbe("probe 7", 7),
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


@socket.on('action')
def on_action(action):
    print(action)
    for module in module_instances:
        module.receive_action(action["module"], action["data"])

# @app.route('/api/valve/<name>', methods=['GET', 'POST'])
# def api_valve(name):
#     global valves
#     valve = valves.get(name)
#     if valve is None:
#         return ""
#     if request.method == "GET":
#         return json.dumps(valve.json)
#     if request.method == "POST":
#         target = request.form.get("target")
#         valve.set_percent(int(target))
#         return ""
#
#
# @app.route('/api/pump/<name>')
# @requires_auth
# def api_pump(name):
#
#     pumps = {
#         "coolant": coolant_pump,
#         "wash": wash_bilge,
#     }
#     pump = pumps.get(name)
#
#     if pump is None:
#         return "500"
#
#     state = request.args.get("state")
#     if state not in ["on", "off"]:
#         return "500"
#
#     if state == "on":
#         print("turned pump "+name+" on")
#         pump.on()
#     if state == "off":
#         print("turned pump "+name+" off")
#         pump.off()
#
#     return "200"
#
#
# @app.route('/api/wash', methods=["POST"])
# @requires_auth
# def api_wash():
#     rate = request.args.get("rate")
#     print("attempting to wash input rate updated to "+str(rate))
#     try:
#         rate = float(rate)
#     except:
#         return "500"
#
#     if rate < 0 or rate > 100:
#         return "500"
#
#     # TODO set wash input rate
#     print("wash input rate updated to "+str(rate))
#     wash_bilge.set_rate(rate)
#
#     return "200"
#


if __name__ == '__main__':
    # app.run(use_reloader=True, port=5000)
    socket.run(app, use_reloader=True, host="0.0.0.0", port=5000)


