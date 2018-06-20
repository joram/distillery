import time
import json
import threading
import random
import datetime
import ads1256
import signal
from flask import Flask, render_template
from temperatureStore import TemperatureStore

app = Flask(
    __name__,
    static_url_path="/static",
    static_folder="static",
)

running = True
tempStore = TemperatureStore()

@app.route('/')
def temperature():
    return render_template('temperature.html')

@app.route('/api/temperatures')
def api_temperature():
    return json.dumps(tempStore.json())

def poll_temp():
    while running:
        for channel in range(0,8):
            temperature = ads1256.read_channel(channel)
            channel_name = "probe "+str(channel)
            tempStore.add_temp(channel_name, temperature)
            time.sleep(10)
            if not running:
                break
    print "done polling"

def handler(signum, fram):
    global running
    running = False


if __name__ == '__main__':
    for s in [signal.SIGUSR1, signal.SIGUSR2, signal.SIGALRM, signal.SIGINT, signal.SIGQUIT]:
        signal.signal(s, handler)    

    gain = 1
    sps = 25
    ads1256.start(str(gain), str(sps))
    t = threading.Thread(target=poll_temp, args=())
    t.start()
    
    app.run(
        debug=True,
        host='0.0.0.0',
    )
