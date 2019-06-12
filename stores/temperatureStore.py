import time
import threading
from stores.timeSeriesStore import TimeSeriesStore
import signal
ADS1256_INITIALIZED = False


def init_board(gain=1, sps=25):
    try:
        import ads1256
    except:
        print("unable to import ads1256")
        return
    global ADS1256_INITIALIZED
    if ADS1256_INITIALIZED:
        print("not double initing board...")
        return
    print("initing board...")
    ads1256.start(str(gain), str(sps))
    ADS1256_INITIALIZED = True
    print("inited board...")


class TemperatureStore(TimeSeriesStore):

    RUNNING = False

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

        init_board()

    def start(self):
        if self.RUNNING:
            raise Exception("already running")
        t = threading.Thread(target=self.poll_temp, args=())
        t.daemon = True
        self.RUNNING = True
        t.start()

    def _read_value(self):
        if not ADS1256_INITIALIZED:
            return 1
        import ads1256
        value = ads1256.read_channel(self.pin)
        return value

    def poll_temp(self):
        while self.RUNNING:
            value = self._read_value()
            temp = self.m*value + self.b
            print("pin:%d val:%s Celcius:%sc" % (self.pin, value, temp))
            self.add_value(temp)
            time.sleep(self.sleep)
