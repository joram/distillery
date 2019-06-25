import atexit
from modules.valve import Valve
from modules.float_sensor import FloatSensor
from modules.relay import Relay
import pins


class Bilge(object):

  def __init__(self, float_pin=18, valve_open_pin=19, valve_closed_pin=26, valve_motor_index=3, valve_calibrate=True):
    self.pump = Relay(pins.WASH_PUMP)
    self.valve = Valve(valve_open_pin, valve_closed_pin, valve_motor_index, valve_calibrate)
    self.rate = 0
    self._enabled = False
    self.off()
    self.on()
#    self.set_rate(50)
    self.float_sensor = FloatSensor(float_pin, self.floating, self.not_floating)
    atexit.register(self.shutdown)

  def on(self):
    self._enabled = True
  
  def off(self):
    self._enabled = False
    self.pump.off()
    self.set_rate(0)

  def set_rate(self, rate):
    print("draining bilge at %s ml/min" % rate)
    if self._enabled:
      self.valve.set_percent(rate)
      self.rate = rate
   
  def shutdown(self):
    print("shutting down bilge pump")
    self.pump.off()

  def floating(self):
    print("bilge is full")
    if self._enabled:
      self.pump.off()
  
  def not_floating(self):
    print("bilge is not full")
    if self._enabled:
      self.pump.on()

