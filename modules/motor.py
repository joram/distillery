#!/usr/bin/python
import atexit

_MH = None


def get_motorhat():
    global _MH
    if _MH is None:
        from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
        _MH = Adafruit_MotorHAT(addr=0x60)
    return _MH


class MockDCMotor(object):
    def __init__(self, controller, num):
        pass

    def run(self, command):
        pass

    def setSpeed(self, speed):
        pass


def turn_off_motors():
    try:
        from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
        get_motorhat().getMotor(1).run(Adafruit_MotorHAT.RELEASE)
        get_motorhat().getMotor(2).run(Adafruit_MotorHAT.RELEASE)
        get_motorhat().getMotor(3).run(Adafruit_MotorHAT.RELEASE)
        get_motorhat().getMotor(4).run(Adafruit_MotorHAT.RELEASE)
    except:
        pass


def get_motor(i):
    if i not in [1, 2, 3, 4]:
        raise Exception("There are only four motors.")
    try:
        return get_motorhat().getMotor(i)
    except:
        return MockDCMotor(None, i)


atexit.register(turn_off_motors)

