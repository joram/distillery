from modules.valve import Valve
from modules.float_sensor import FloatSensor

class Bilge(object):

  def __init__(self, float_pin=18, valve_open_pin=21, valve_closed_pin=20, valve_motor_index=3, valve_calibrate=True):
    print("passing float pint to sensor", float_pin)
    self.float_sensor = FloatSensor(float_pin)
    self.valve = Valve(valve_open_pin, valve_closed_pin, valve_motor_index, valve_calibrate)
