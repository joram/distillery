import datetime
from ads1256 import ADS1256
import threading
import time

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

        if self.last_poll is None:
            self.last_poll = now
            self._data = self.ADC.ADS1256_GetAll()
            return

        delta = self.last_poll - now
        if delta.total_seconds() > self.min_seconds_between_polls:
            self.last_poll = now
            self._data = self.ADC.ADS1256_GetAll()

    def get_value(self, pin):
        self._debounced_poll()
        if self._data is None or pin not in self._data:
            return None, None
        return self._data[pin], self.last_poll


class TemperatureProbe(object):

    TEMPERATURE_DATA = []

    def __init__(self, pin=0, sleep=5, calibrations=((0, 0), (1, 1))):
        self.pin = pin
        self.name = "Pin %d" % pin
        self.sleep = sleep
        self.calibrations = calibrations

        # pre-compute for temperature calc
        (d1, d2) = self.calibrations
        (y1, x1) = d1
        (y2, x2) = d2
        yd = float(y2 - y1)
        xd = float(x2 - x1)
        self.m = yd/xd
        self.b = float(y1) - self.m*float(x1)

    def json(self, dt=None):
        self.get_value()
        jsonVals = []
        for val in self.TEMPERATURE_DATA:
            if dt is None or val["t"] > dt:
                tStr = val["t"].strftime("%Y-%m-%dT%H:%M:%SZ")
                jsonVals.append({
                    "t": tStr,
                    "y": val["y"],
                })
        return jsonVals

    def current_temperature(self):
        value, timestamp = get_analog_value_reader().get_value(self.pin)
        if value is None:
            return None, None, None
        temp = self.m * value + self.b
        return temp, value, timestamp

    @property
    def latest_value(self):
        if len(self.TEMPERATURE_DATA) <= 0:
            return -1
        return self.TEMPERATURE_DATA[-1]["y"]

    def get_value(self):
        temp, value, timestamp = self.current_temperature()
        print("pin:%d v:%s t:%sc" % (self.pin, value, temp))
        self.TEMPERATURE_DATA.append({
            "t": timestamp,
            "y": value,
        })
