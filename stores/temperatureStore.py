import time
import ads1256
import threading
from timeSeriesStore import TimeSeriesStore

ADS1256_INITIALIZED = False


def init_board(gain=1, sps=25):
    global ADS1256_INITIALIZED
    if ADS1256_INITIALIZED:
        print "not double initing board..."
        return
    print "initing board..."
    ADS1256_INITIALIZED = True
    ads1256.start(str(gain), str(sps))
    print "inited board..."


class TemperatureStore(TimeSeriesStore):

    def __init__(self, pin=0, sleep=5, calibrations=((0,0), (1,1)), debug=False):
        self.pin = pin
        self.name = "Pin %d" % pin
        self.sleep = sleep
        self.calibrations = calibrations
        self.running = False
        self.debug = debug

        # pre-compute for temperature calc
        (d1, d2) = self.calibrations
        (y1, x1) = d1
        (y2, x2) = d2
        yd = float(y2 - y1)
        xd = float(x2 - x1)
        self.m = yd/xd
        self.b = float(y1) - self.m*float(x1)

        init_board()
        self.start()

    def start(self):
        if self.running:
            raise Exception("already running")
        t = threading.Thread(target=self.poll_temp, args=())
        t.daemon = True
        self.running = True
        t.start()

    def poll_temp(self):
        while self.running:
            value = ads1256.read_channel(self.pin)
            temp = self.m*value + self.b
            if self.debug:
              print("pin:%d val:%f Celcius:%fc" % (self.pin, value, temp))
            self.add_value(temp)
            time.sleep(self.sleep)
