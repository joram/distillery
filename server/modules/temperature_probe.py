import time
import datetime
from ads1256 import ADS1256
from modules import BaseModule
AVR = None


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

    TEMPERATURE_DATA = []

    def __init__(self, name, pin=0, sleep=5, calibrations=((0, 0), (1, 1))):
        self.pin = pin
        self.name = name
        self.sleep = sleep
        self.calibrations = calibrations
        self.thread = None

        # pre-compute for temperature calc
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

    def emit(self, socket):
        self._emit_value_update(socket, "temperature_probes", self.name, self.value)
        if self.thread is None:
            # background thread emitting state
            self.socket = socket
            self.thread = socket.start_background_task(self.poll)

    def poll(self):
        while True:
            time.sleep(1)
            self.emit(self.socket)

