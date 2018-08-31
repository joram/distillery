#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor 
import atexit

MH = Adafruit_MotorHAT(addr=0x60)


def turnOffMotors():
  MH.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
  MH.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
  MH.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
  MH.getMotor(4).run(Adafruit_MotorHAT.RELEASE)


def getMotor(i):
  if i not in [1,2,3,4]:
    raise Exception("There are only four motors.")
  return MH.getMotor(i)


atexit.register(turnOffMotors)

