import time
import datetime
from ads1256 import ADS1256
from modules import BaseModule
AVR = None

default_calibration = ((20, 3567560), (73, 2816778))


t1 = 25.7
v1 = [3540587.75, 2274642.625, 594823.375, 596040.625, 587538.25, 588527.625, 586106.25, 588199.625]

# TODO: redo
t2 = 94.9
v2 = [2305418.872, 1458037.319, 79212, 80202.44681, 80215.44681, 79026.46809, 79404.40426, 2027174.404]

calibrations = {}
for i in range(0, 8):
  calibrations[i] = ((t1, v1[i]), (t2+1, v2[i]+1))


def get_analog_value_reader():
    global AVR
    if AVR is None:
        AVR = AnalogValuesReader()
    return AVR


class AnalogValuesReader(object):

    def __init__(self):
        self.last_poll = None
        self.min_seconds_between_polls = 1
        self._data = None
        self._avg_data = None

        self.ADC = ADS1256.ADS1256()
        self.ADC.ADS1256_init()

    def _debounced_poll(self):
        now = datetime.datetime.now()

        def _should_poll():
            if self.last_poll is None:
                return True
            delta = now - self.last_poll
            if delta.total_seconds() > self.min_seconds_between_polls:
                return True
            return False

        if _should_poll():
            self.last_poll = now
            self._data = self.ADC.ADS1256_GetAll()
            if(self._avg_data == None):
                self._avg_data = self._data

            ratio = 0.01
            for i in range(0, len(self._data)):
                self._avg_data[i] = (1.0-ratio)*self._avg_data[i] + ratio*self._data[i]

            print(self._data)

    def get_value(self, pin):
        self._debounced_poll()
        if self._data is None:
            return None, None
        return self._avg_data[pin]


class TemperatureProbe(BaseModule):

    def __init__(self, name, pin=0, sleep=5):
        self.pin = pin
        self.name = name
        self.sleep = sleep
        self.thread = None
        self.socket = None
        self.offset = 0

        # pre-compute for temperature calc
        #self.calibrations = calibrations[self.pin]
        self.calibrations = calibrations[6]
        (d1, d2) = self.calibrations
        (y1, x1) = d1
        (y2, x2) = d2
        yd = float(y2 - y1)
        xd = float(x2 - x1)
        self.m = yd/xd
        self.b = float(y1) - self.m*float(x1)

    @property
    def value(self):
        return get_analog_value_reader().get_value(self.pin)

    @property
    def temperature(self):
        return (self.m * self.value) + self.b + self.offset

    def emit(self, socket):
        self._emit_value_update(socket, "temperature_probes", self.name, self.temperature)
        if self.thread is None:
            self.socket = socket
            self.thread = socket.start_background_task(self.poll)

    def receive_action(self, module_name, data):
        if module_name == "temperature":
            actual_temp = float(data["current_temperature"])
            self.offset += actual_temp - self.temperature

    def poll(self):
        while True:
            time.sleep(self.sleep)
            self.emit(self.socket)
