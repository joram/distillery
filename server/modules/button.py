import time
import threading
from RPi import GPIO

BCM_SET = False
BUTTONS = {}


def pressed(pin):
    global BUTTONS
    button = BUTTONS[pin]
    button.changed()


class Button(object):

    def __init__(self, pin, inverse=False, sleep_ms=500):
        global BCM_SET
        global BUTTONS

        if not BCM_SET:
            GPIO.setmode(GPIO.BCM)
            BCM_SET = True

        self.pin = pin
        self.value = -1
        self.sleep_ms = sleep_ms
        self.inverse = inverse
        BUTTONS[pin] = self
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(pin, GPIO.RISING, callback=pressed)
        self.changed()

    def changed(self):
        value = GPIO.input(self.pin)
        if value == self.value:
            return

        self.value = value
        if self.is_pressed:
            self.pressed()
        else:
            self.unpressed()

    def pressed(self):
        print("pressed ", self.pin)

    def unpressed(self):
        print("unpressed ", self.pin)

    @property
    def is_pressed(self):
      if self.inverse:
        return self.value == 0
      return self.value == 1
        
