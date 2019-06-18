import RPi.GPIO as GPIO


class Relay(object):

    def __init__(self, pin=21):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

    def on(self):
        GPIO.output(self.pin, GPIO.LOW)

    def off(self):
        GPIO.output(self.pin, GPIO.HIGH)

import pins
coolant_pump = Relay(pins.COOLANT_PUMP)
wash_pump = Relay(pins.WASH_PUMP)
