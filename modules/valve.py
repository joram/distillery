import time
from button import Button
from motor import getMotor
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

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
    self.calibrate()


  def test_calibration(self):
    while not self.open_button.pressed:
      self.tick_open()
      print "%d%% open" % self.percent_open

    while not self.closed_button.pressed:
      self.tick_closed()
      print "%d%% open" % self.percent_open

  def _tick(self, direction):
    if self.currentDir != direction:
      self.motor.run(direction)
    self.currentDir = direction
    self.motor.setSpeed(self.tickSpeed)
    time.sleep(self.tickSleep)
    self.motor.setSpeed(0)

  def tick_open(self):
    self.currentTick += 1
    self._tick(Adafruit_MotorHAT.FORWARD)
  
  def tick_closed(self):
    self.currentTick -= 1
    self._tick(Adafruit_MotorHAT.BACKWARD)

  def calibrate(self):
    while not self.open_button.pressed:
      self.tick_open()
    self.totalTicks = 0
    while not self.closed_button.pressed:
      self.tick_closed()
      self.totalTicks += 1
    self.currentTick = 0

  @property
  def percent_open(self):
    return 100*self.currentTick/self.totalTicks
