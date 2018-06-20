import random
import datetime
from timeSeriesStore import TimeSeriesStore

class TemperatureStore(TimeSeriesStore):

    RUNNING = False
    INIT_BOARD = False

    def start(self):
        self.RUNNING = True
        if !self.INIT_BOARD:
            self._init_board()

    def stop(self):
        self.RUNNING = False

    def poll_temp(channel=0, sleep_s=1):
        while self.RUNNING:
            temperature = ads1256.read_channel(channel)
            channel_name = "probe "+str(channel)
            self.add_temp(channel_name, temperature)
            time.sleep(sleep_s)
            if not SELF.RUNNING:
                break
        print "done polling"
    
    def _init_board(self):
        print "initing board..."
        print "inited board..."
