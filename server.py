import time
import json
import threading
import random
import datetime
import ads1256
import signal
from flask import Flask, render_template, request
from temperatureStore import TemperatureStore


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

def handler(signum, fram):
    for t in temperatureStores:
        t.stop()
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

if __name__ == '__main__':
    for s in [signal.SIGUSR1, signal.SIGUSR2, signal.SIGALRM, signal.SIGINT, signal.SIGQUIT]:
        signal.signal(s, handler)    

    for t in temperatureStores:
        t.start()
    app.run(
        debug=True,
        host='0.0.0.0',
    )
