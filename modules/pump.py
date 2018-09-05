import time
import threading
from button import Button
from motor import getMotor
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

FORWARD = Adafruit_MotorHAT.FORWARD
STOP= Adafruit_MotorHAT.RELEASE


class Pump(object):

  def __init__(self, motor_index=4):
    self.motor = getMotor(motor_index)

  def on(self):
    self.motor.setSpeed(255)
    self.motor.run(FORWARD)

  def off(self):
    self.motor.setSpeed(0)
    self.motor.run(STOP)


if __name__ == "__main__":
  p = Pump()
  p.on()
  time.sleep(1)
  p.off()
