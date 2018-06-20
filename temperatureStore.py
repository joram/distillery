import time
import ads1256
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
        for i in range(0,3):
            threading.Thread(target=self.poll_temp, args=(i, 5)).start()
        
    def stop(self):
        self.RUNNING = False

    def poll_temp(self, channel=0, sleep_s=1):
        while self.RUNNING:
            temperature = ads1256.read_channel(channel)
            channel_name = "probe "+str(channel)
            self.add_temp(channel_name, temperature)
            time.sleep(sleep_s)
            if not self.RUNNING:
                break
        print "done polling"
    
    def _init_board(self):
        print "initing board..."
        gain = 1
        sps = 25
        ads1256.start(str(gain), str(sps))
        print "inited board..."
