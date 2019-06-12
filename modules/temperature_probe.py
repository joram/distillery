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
        print("starting avr")
        self._data = {}
        for i in range(0, 8):
            self._data[i] = []
        self.max_data = 100
        self.ADC = ADS1256.ADS1256()
        self.ADC.ADS1256_init()
        t = threading.Thread(target=self._poll, args=())
        t.daemon = True
        self.RUNNING = True
        t.start()

    def _poll(self):
        while True:
            time.sleep(5)
            self.take_reading()

    def take_reading(self):
        readings = self.ADC.ADS1256_GetAll()
        for i in range(0, 8):
            self._data[i].append({
                "reading": readings[i],
                "time": datetime.datetime.now(),
            })
            while len(self._data[0]) > self.max_data:
                del self._data[0]

    def get_latest(self, pin):
        if pin not in self._data:
            return None
        if len(self._data[pin]) == 0:
            return None
        return self._data[pin][-1]


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

    @property
    def latest_value(self):
        if len(self.TEMPERATURE_DATA) <= 0:
            return -1
        return self.TEMPERATURE_DATA[-1]["y"]

    def get_value(self):
        data = get_analog_value_reader().get_latest(self.pin)
        if data is None:
            return
        value = data["reading"]
        time = data["time"]
        temp = self.m * value + self.b
        print("pin:%d val:%s Celcius:%sc" % (self.pin, value, temp))

        self.TEMPERATURE_DATA.append({
            "t": time,
            "y": value,
        })
