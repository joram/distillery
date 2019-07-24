import atexit
from modules.valve import Valve
from modules.float_sensor import FloatSensor
from modules.relay import Relay
from modules.base_module import BaseModule
import pins


class Bilge(BaseModule):

  def __init__(self, name, float_pin=18, valve_open_pin=26, valve_closed_pin=19, valve_motor_index=3, valve_calibrate=True):
    self.name = name
    self.pump = Relay(pins.WASH_PUMP)
    self.valve = Valve(valve_open_pin, valve_closed_pin, valve_motor_index, valve_calibrate)
    self.rate = 0
    self.socket = None
    self._enabled = False
    self.off()
    self.float_sensor = FloatSensor(float_pin, self.floating, self.not_floating)
    atexit.register(self.shutdown)

  def on(self):
    self._enabled = True
    if self.socket is not None:
      self.emit(self.socket)

  def off(self):
    self._enabled = False
    self.pump.off()
    self.set_rate(0)
    if self.socket is not None:
      self.emit(self.socket)

  def emit(self, socket):
    self._emit_value_update(socket, self.name, "enabled", self._enabled)
    self._emit_value_update(socket, self.name, "floating", self.float_sensor.is_floating())
    self._emit_value_update(socket, self.name, "open", self.valve.target_percent)
    self.socket = socket

  def process_action(self, action):
    enabled = action.get("enabled")
    if enabled is not None:
      if enabled is True:
        self.on()
        return
      if enabled is False:
        self.off()
        return
      raise Exception("not a boolean", enabled)

    set_rate = action.get("set_rate")
    if set_rate is not None:
      self.set_rate(set_rate)
      return

    raise Exception("unknown action", action)

  def set_rate(self, rate):
    print("draining bilge at %s ml/min" % rate)
    if self._enabled:
      self.valve.set_percent(rate)
      self.rate = rate
      if self.socket is not None:
        self.emit(self.socket)

  def shutdown(self):
    print("shutting down bilge pump")
    self.pump.off()

  def floating(self):
    if self._enabled:
      self.pump.off()
    if self.socket is not None:
      self.emit(self.socket)

  def not_floating(self):
    if self._enabled:
      self.pump.on()
    if self.socket is not None:
      self.emit(self.socket)

