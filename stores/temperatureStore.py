import time
import ads1256
import threading
from timeSeriesStore import TimeSeriesStore

ADS1256_INITIALIZED = False

calibrations = (
#  (1.0, 3604000),
#	(91.5, 2650000),
  (28, 3486131),
  (73, 2816778),
)


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

    def latest_temperature(self):
       # y = mx + b
       # b = y intercept
       # y = temperature
       # x = raw value
       (d1, d2) = self.calibrations
       (y1, x1) = d1
       (y2, x2) = d2
       yd = float(y2 - y1)
       xd = float(x2 - x1)
       m = yd/xd
       b = float(y1) - m*float(x1)
       x = self.latest_value(self.name)
       y = m*x+b
#       print "y(%f) = m(%f)*x(%f) + b(%f)\t\t and yd(%f), xd(%f)" % (y, m, x, b, yd, xd)
       return y


if __name__ == "__main__":
    print "calibrating"
    for tv in calibrations:
        t, v = tv
        print "\tT:%f\tV:%f" % (t,v)
        ts = TemperatureStore(0, 1, calibrations)
        ts.start()

    while True:
        time.sleep(1)
        print "value: %d\t temperature: %0.3f" % (
            ts.latest_value(ts.name),
    		    ts.latest_temperature()
     		)

