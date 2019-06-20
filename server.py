#!/usr/bin/env python3
import datetime
from flask import Flask, render_template, request
import json
import sys
import os
from git import Repo
try:
    from RPi import GPIO
except:
    print("faking rpi")
    import fake_rpi
    sys.modules['RPi'] = fake_rpi.RPi  # Fake RPi (GPIO)
    sys.modules['smbus'] = fake_rpi.smbus  # Fake smbus (I2C)
from modules.temperature_probe import TemperatureProbe
from modules.button import Button
from modules.valve import Valve
from modules.relay import Relay
import pins

calibrations = (
#  (1.0, 3604000),
# (91.5, 2650000),
  (28, 3486131),
  (73, 2816778),
)

repo_path = os.path.dirname(os.path.abspath(__file__))
repo = Repo(repo_path)
temperatureProbes = []
valves = {}

coolant_pump = Relay(pins.COOLANT_PUMP)
wash_pump = Relay(pins.WASH_PUMP)

app = Flask(
    __name__,
    static_url_path="/static",
    static_folder="static",
)


@app.route('/api/valve/<name>', methods=['GET', 'POST'])
def api_valve(name):
    global valves
    valve = valves.get(name)
    if valve is None:
        return ""
    if request.method == "GET":
        return json.dumps(valve.json)
    if request.method == "POST":
        target = request.form.get("target")
        valve.set_percent(int(target))
        return ""


@app.route('/')
def temperature():
    return render_template('index.html')


def _exec_sh(bashCommand):
    import subprocess
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return output, error


@app.route('/api/git/status')
def git_status():
    commits_behind = repo.iter_commits('master..origin/master')
    num_commits_behind = len(list(commits_behind))
    commits_ahead = repo.iter_commits('origin/master..master')
    num_commits_ahead = len(list(commits_ahead))
    if num_commits_behind == 0 and num_commits_ahead == 0:
        return ""
    return "%d behind and %d ahead" % (num_commits_behind, num_commits_ahead)


@app.route('/api/git/update')
def git_update():
    _exec_sh("git pull origin master")
    _exec_sh("pip install -r requirements.txt")
    return str(True)


@app.route('/api/pump/<name>')
def api_pump(name):

    if name != "coolant":
        return "500"
    pump = coolant_pump

    state = request.args.get("state")
    if state not in ["on", "off"]:
        return "500"

    if state == "on":
        print("turned pump "+name+" on")
        pump.on()
    if state == "off":
        print("turned pump "+name+" off")
        pump.off()

    return "200"


@app.route('/api/wash', methods=["POST"])
def api_wash():
    rate = request.args.get("rate")
    print("attempting to wash input rate updated to "+str(rate))
    try:
        rate = float(rate)
    except:
        return "500"

    if rate < 0 or rate > 100:
        return "500"

    # TODO set wash input rate
    print("wash input rate updated to "+str(rate))

    return "200"


@app.route('/api/temperatures')
def api_temperature():
    global temperatureProbes
    dt = request.args.get("dt")
    if dt:
        dt = datetime.datetime.strptime(dt, "%Y-%m-%dT%H:%M:%SZ")
    data = {}
    for t in temperatureProbes:
        data[t.name] = t.json(dt)
    return json.dumps(data)


if __name__ == "__main__":
    print("starting...")
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        print("werkzeug...")
        for i in range(0, 8):
            print("temperature probe "+str(i))
            ts = TemperatureProbe(pin=i, sleep=2, calibrations=calibrations)
            temperatureProbes.append(ts)
    app.run(
        debug=True,
        host='0.0.0.0',
    )
