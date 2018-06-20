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

    def _init_board(self):
        print "initing board..."
        print "inited board..."
