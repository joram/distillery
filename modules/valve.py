import time
import threading
from button import Button
from motor import getMotor
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

OPEN = Adafruit_MotorHAT.FORWARD
CLOSE = Adafruit_MotorHAT.BACKWARD

class Valve(object):

  def __init__(self, open_pin=21, closed_pin=20, motor_index=3):
    self.open_button = Button(open_pin)
    self.closed_button = Button(closed_pin)
    self.motor = getMotor(motor_index)
    self.totalTicks = 0
    self.currentTick = 0
    self.currentDir = None
    self.tickSleep = 0.1
    self.tickSpeed = 50
    self.targetPercent = 0
    self.fast_calibrate()
    t = threading.Thread(target=self._adjust_valve, args=())
    t.daemon = True
    t.start()

  def _adjust_valve(self):
    while True:
      if self.targetPercent == self.get_percent():
        time.sleep(1)
        continue
      if self.targetPercent > self.get_percent():
        self.tick_open()
      if self.targetPercent < self.get_percent():
        self.tick_closed()


  def fast_calibrate(self):
    while self.tick_closed():
      continue
    self.totalTicks = 167
    self.currentTick = 0
    self.targetPercent = 0

  @property
  def json(self):
    return {
      "status": self.status,
      "current": self.get_percent(),
      "target": self.targetPercent,
    }

  @property
  def status(self):
    if self.targetPercent > self.get_percent():
      return "opening"
    if self.targetPercent < self.get_percent():
      return "closing"
    return "idle"

  def _tick(self, direction):
    
    if self.currentDir != direction:
      self.motor.run(direction)
    self.currentDir = direction
    self.motor.setSpeed(self.tickSpeed)
    time.sleep(self.tickSleep)
    self.motor.setSpeed(0)

  def tick_open(self):
    if self.open_button.pressed:
      return False
    self.currentTick += 1
    self._tick(OPEN)
    return True
  
  def tick_closed(self):
    if self.closed_button.pressed:
      return False
    self.currentTick -= 1
    self._tick(CLOSE)
    return True

  def calibrate(self):
    while self.tick_open():
      continue

    self.totalTicks = 0
    while self.tick_closed():
      self.totalTicks += 1
    self.currentTick = 0

  def set_percent(self, target):
    self.targetPercent = target

  def get_percent(self):
    return 100*self.currentTick/self.totalTicks
