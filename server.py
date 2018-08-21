import json
import datetime
from flask import Flask, render_template, request
from stores.temperatureStore import TemperatureStore


temperatureStores = [TemperatureStore(i) for i in range(0,5)]
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
    dt = request.args.get("dt")
    if dt:
        dt = datetime.datetime.strptime(dt, "%Y-%m-%dT%H:%M:%SZ")
    data = {}
    for t in temperatureStores:
        data.update(t.json(dt))
    return json.dumps(data)


if __name__ == '__main__':
    for t in temperatureStores:
        t.start()
    app.run(
        debug=True,
        host='0.0.0.0',
    )
