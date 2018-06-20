import random
import datetime
import threading
from timeSeriesStore import TimeSeriesStore

class TemperatureStore(TimeSeriesStore):

    RUNNING = False
    INIT_BOARD = False

    def start(self):
        self.RUNNING = True
        if not self.INIT_BOARD:
            self.INIT_BOARD = True
            self._init_board()
        threading.Thread(target=self.poll_temp, args=(self, 0, 5)).start()
        
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
        gain = 1
        sps = 25
        ads1256.start(str(gain), str(sps))
        print "inited board..."
