from wrapped_rpi_gpio import GPIO

BCM_SET = False
BUTTONS = {}


def _pin_changed(pin):
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
        GPIO.add_event_detect(pin, GPIO.RISING, callback=_pin_changed)
        self.changed()

    def changed(self):
        value = GPIO.input(self.pin)
        if value == self.value:
            return
        self.value = value

        if self.is_pressed:
            print("pressed ", self.pin)
            self.pressed_callback()
            return

        print("unpressed ", self.pin)
        self.unpressed_callback()

    def pressed_callback(self):
        pass

    def unpressed_callback(self):
        pass

    @property
    def is_pressed(self):
      if self.inverse:
        return self.value == 0
      return self.value == 1
        
