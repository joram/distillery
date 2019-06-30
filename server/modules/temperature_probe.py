import time
import datetime
from ads1256 import ADS1256
from modules import BaseModule
AVR = None

calibrations = {
    0: ((20, 3567560), (73, 2816778)),
    1: ((20, 4890208), (73, 2816778)),
    2: ((20, 697096), (73, 2816778)),
    3: ((20, 689629), (73, 2816778)),
    4: ((20, 680261), (73, 2816778)),
    5: ((20, 675023), (73, 2816778)),
    6: ((20, 2025773), (73, 2816778)),
    7: ((20, 2026363), (73, 2816778)),
}


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
            print(self._data)

    def get_value(self, pin):
        self._debounced_poll()
        if self._data is None:
            return None, None
        return self._data[pin]


class TemperatureProbe(BaseModule):

    def __init__(self, name, pin=0, sleep=5):
        self.pin = pin
        self.name = name
        self.sleep = sleep
        self.thread = None
        self.socket = None

        # pre-compute for temperature calc
        self.calibrations = calibrations[self.pin]
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
        return (self.m * self.value) + self.b

    def emit(self, socket):
        self._emit_value_update(socket, "temperature_probes", self.name, self.temperature)
        if self.thread is None:
            self.socket = socket
            self.thread = socket.start_background_task(self.poll)

    def poll(self):
        while True:
            time.sleep(self.sleep)
            self.emit(self.socket)
