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
    import fake_rpi
    sys.modules['RPi'] = fake_rpi.RPi  # Fake RPi (GPIO)
    sys.modules['smbus'] = fake_rpi.smbus  # Fake smbus (I2C)
from stores.temperatureStore import TemperatureStore
from modules.button import Button
from modules.valve import Valve


calibrations = (
#  (1.0, 3604000),
# (91.5, 2650000),
  (28, 3486131),
  (73, 2816778),
)

repo_path = os.path.dirname(os.path.abspath(__file__))
repo = Repo(repo_path)
temperatureStores = []
valves = {}

app = Flask(
    __name__,
    static_url_path="/static",
    static_folder="static",
)


@app.route('/api/valve/<name>', methods=['GET', 'POST'])
def api_valve(name):
    global valves
    valve = valves[name]
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
    return f"{num_commits_behind} behind and {num_commits_ahead} ahead"


@app.route('/api/git/update')
def git_update():
    _exec_sh("git pull origin master")
    _exec_sh("pip install -r requirements.txt")
    return str(True)


@app.route('/api/temperatures')
def api_temperature():
    global temperatureStores
    dt = request.args.get("dt")
    if dt:
        dt = datetime.datetime.strptime(dt, "%Y-%m-%dT%H:%M:%SZ")
    data = {}
    for t in temperatureStores:
        data[t.name] = t.json(dt)
    return json.dumps(data)


if __name__ == "__main__":
    app.run(
        debug=True,
        host='0.0.0.0',
    )
