from modules.base_module import BaseModule
from wrapped_rpi_gpio import *


class Relay(BaseModule):

    def __init__(self, name, pin=21):
        print(name)
        self.name = name
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self._is_on = False
        self.socket = None
        self.off()

    def on(self):
        GPIO.output(self.pin, GPIO.LOW)
        self._is_on = True
        if self.socket is not None:
            self.emit(self.socket)

    def off(self):
        GPIO.output(self.pin, GPIO.HIGH)
        self._is_on = False
        if self.socket is not None:
            self.emit(self.socket)

    def emit(self, socket):
        self.socket = socket
        self._emit_value_update(socket, self.name, "enabled", self._is_on)

    def process_action(self, action):
        if action is True:
            self.on()
            return
        if action is False:
            self.off()
            return
        raise Exception("not a boolean", action)

#coolant_pump = Relay(pins.COOLANT_PUMP)
#wash_pump = Relay(pins.WASH_PUMP)
