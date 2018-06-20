import time
import json
import threading
import random
import datetime
import ads1256
import signal
from flask import Flask, render_template, request
from temperatureStore import TemperatureStore

tempStore = TemperatureStore()
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
    return json.dumps(tempStore.json())

def handler(signum, fram):
    tempStore.stop()
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

if __name__ == '__main__':
    for s in [signal.SIGUSR1, signal.SIGUSR2, signal.SIGALRM, signal.SIGINT, signal.SIGQUIT]:
        signal.signal(s, handler)    

    tempStore.start() 
    app.run(
        debug=True,
        host='0.0.0.0',
    )
