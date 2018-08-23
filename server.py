import os
import json
import datetime
from flask import Flask, render_template, request
from stores.temperatureStore import TemperatureStore


calibrations = (
#  (1.0, 3604000),
# (91.5, 2650000),
  (28, 3486131),
  (73, 2816778),
)
		

temperatureStores = []

app = Flask(
    __name__,
    static_url_path="/static",
    static_folder="static",
)


@app.route('/')
def temperature():
    return render_template('temperature.html')


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
    print "main!"
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        ts = TemperatureStore(pin=0, sleep=2, calibrations=calibrations)
        ts.start()
        temperatureStores.append(ts)

    app.run(
        debug=True,
        host='0.0.0.0',
    )
