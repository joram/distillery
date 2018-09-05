#!/usr/bin/env python
import os
import json
import datetime
from flask import Flask, render_template, request
from stores.temperatureStore import TemperatureStore
from modules.button import Button
from modules.valve import Valve

calibrations = (
#  (1.0, 3604000),
# (91.5, 2650000),
  (28, 3486131),
  (73, 2816778),
)
		

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


if __name__ == '__main__':
  if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
#        ts = TemperatureStore(pin=0, sleep=2, calibrations=calibrations)
#        ts.start()
#        temperatureStores.append(ts)
#        button = Button(20)
#        button = Button(21)i
    global valves  
    valves["input"] = Valve()

  app.run(
    debug=True,
    host='0.0.0.0',
  )
