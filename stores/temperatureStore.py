import time
import ads1256
import threading
from timeSeriesStore import TimeSeriesStore

ADS1256_INITIALIZED = False


def init_board(gain=1, sps=25):
    print "initing board..."
    ads1256.start(str(gain), str(sps))
    print "inited board..."


class TemperatureStore(TimeSeriesStore):

    RUNNING = False

    def __init__(self, pin=0, sleep=5, calibrations=((0,0), (1,1))):
        global ADS1256_INITIALIZED
        self.pin = pin
        self.name = "Pin %d" % pin
        self.sleep = sleep
        self.calibrations = calibrations

        if not ADS1256_INITIALIZED:
            ADS1256_INITIALIZED = True
            init_board()

    def start(self):
        if self.RUNNING:
            raise Exception("already running")
        t = threading.Thread(target=self.poll_temp, args=())
        t.daemon = True
        self.RUNNING = True
        t.start()

    def poll_temp(self):
        while self.RUNNING:
            value = ads1256.read_channel(self.pin)
            self.add_temp(self.name, value)
            time.sleep(self.sleep)
